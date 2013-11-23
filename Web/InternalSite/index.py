# vim:encoding=utf-8:ts=2:sw=2:expandtab

from Project import *
###############################################################################

@Expose
def Init(self):
  yield
  yield



@Expose
def Request(self):
  yield 
  #----------------------------------------------------------------------------
  self.UI.Title = 'Home'

  #----------------------------------------------------------------------------
  W = self.UI.Body('''
    <h1>A Page</h1>
    <a href="/example1/">Example 1</a>
    
    ''')

  #----------------------------------------------------------------------------

  yield self.UI
