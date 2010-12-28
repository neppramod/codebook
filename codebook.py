#!/usr/bin/env python
'''
Created on Dec 28, 2010

@author: pramod
'''
import sys
try:
  import pygtk
  import gtk
  import gtk.glade  # It may show error in vim but it is required
  pygtk.require("2.0")
except:
  sys.exit(1)

import MySQLdb


class CodeBook:
  def __init__(self):
    self.wTree = gtk.glade.XML("codebook.glade")

    self.counter = 1

    # Create our dictionary and connect it
    dic = {"on_window1_destroy": self.quit,
           "on_btnAdd_clicked": self.on_AddItem}
    self.wTree.signal_autoconnect(dic)

    # Get the treeview (Controller)
    self.treeView = self.wTree.get_widget("codebooktree")

    # Add list columns to the treeview (View)
    # Make as many columns(in simple terms headers) as we will put model in view
    self.AddListColumn("Id", 0)
    self.AddListColumn("Title", 1)
    self.AddListColumn("Catagory", 2)
    self.AddListColumn("Description", 3)

    # Create listStore model for treeview. (Model)
    self.dataList = gtk.ListStore(int, str, str, str)
    self.treeView.set_model(self.dataList)

    # Let's add some data to the model (Add what ever you like tuple, list etc. At list give a list
    conn = MySQLdb.connect(host="localhost", user="root", passwd="mypass", db="codebook_db")
    cursor = conn.cursor()
    cursor.execute("select * from codes")

    for row in cursor.fetchall():
			codes = []
			for data in row:
				codes.append(data)

			codes = codes[0:4]
			self.dataList.append(codes)

    cursor.close()
    conn.close()

  # Our column creator method
  def AddListColumn(self, title, columnId):
    column = gtk.TreeViewColumn(title, gtk.CellRendererText(), text=columnId)
    column.set_resizable(True)
    column.set_sort_column_id(columnId)
    self.treeView.append_column(column)

  def on_AddItem(self, widget):
    """Called when the user wants to add an item"""
    # Create the dialog, show it and store the results
    codeDlg = codeAddDialog()
    result, newCode = codeDlg.run()

    if (result == gtk.RESPONSE_OK):
      """The user clicked Ok, we let's add this to code list"""
      mylist = newCode.getList()
      codeList = newCode.getList()
      mylist = mylist[0:-1]
      mylist.insert(0, self.counter)


      self.counter += 1
      #mylist.append(newCode.getList())
      self.dataList.append(mylist)

      conn = MySQLdb.connect(host="localhost", user="root", passwd="mypass", db="codebook_db")
			# Add to database
      cursor = conn.cursor()

      insertQuery = "insert into codes(title, catagory, description, detail) values('%s','%s', '%s', '%s')" %(codeList[0], codeList[1], codeList[2], codeList[3])

      cursor.execute(insertQuery)

      conn.commit()
      cursor.close()
      conn.close()



  def quit(self, data):
    print "Quiting"
    gtk.main_quit()

class codeAddDialog:
	"""This class is used to show codeAddDlg"""

	def __init__(self, title="", catagory="", description="", detail=""):

		# Setup the glade file
		self.gladefile = "codebook.glade"
		# Setup the code that we will return
		self.code = Code(title, catagory, description, detail)

	def run(self):
		"""This function will show the codeAddDialog"""

		# Load the dialog from the glade file
		self.wTree = gtk.glade.XML(self.gladefile, "codeDlg")

		# Get the actual dialog widget
		self.dlg = self.wTree.get_widget("codeDlg")

		# Get all the Entry Widgets and set their text
		self.enTitle = self.wTree.get_widget("enTitle")
		self.enCatagory = self.wTree.get_widget("enCatagory")
		self.enDescription = self.wTree.get_widget("enDescription")
		self.enDetailTextView = self.wTree.get_widget("enDetailTextView").get_buffer()


		# Run the dialog and store the response
		self.result = self.dlg.run()
		# Get the value of the entry fields
		self.code.title = self.enTitle.get_text()
		self.code.catagory = self.enCatagory.get_text()
		self.code.description = self.enDescription.get_text()
		self.code.detail = self.enDetailTextView.get_text(self.enDetailTextView.get_start_iter(),
						self.enDetailTextView.get_end_iter())


		# We are done with the dialog, destroy it
		self.dlg.destroy()

		# Return the result and the code
		return self.result, self.code

class Code:
	"""This class represents all the code information"""

	def __init__(self, title="", catagory="", description="", detail=""):
		self.title = title
		self.catagory = catagory
		self.description = description
		self.detail = detail

	def getList(self):
		"""This function returns a list made up of the code information.
		It is used to add a code to the dataList easily"""
		return [self.title, self.catagory, self.description, self.detail]


if __name__ == "__main__":
  CodeBook()
  gtk.main()




