# vim:encoding=utf-8:ts=2:sw=2:expandtab

from AppStruct.Util import *
from AppStruct.Web.Util import *
from AppStruct.Web.Response import LayoutResponse
import json 
from AppStruct.UI import StringBuilder, SimpleMenu, ErrorList, InfoList, CSSList, JSList
from urllib.parse import urlsplit, urlencode, urlunsplit, parse_qsl
from collections import namedtuple
from Project import App
###############################################################################

MenuItem2 = namedtuple('MenuItem2', 'ID,URI,Label,Selected')

class MenuItem():
  def __init__(self, *, Label, URI="#", Icon=None, ID=None, Selected=False):
    self.Label = Label
    self.URI = URI
    self.Icon = Icon
    self.ID = ID
    self.Selected = Selected
    self.Submenu = []

  def AddMenu(self, *, Label, URI="#", ID=None, Selected=False):
    self.Submenu.append(MenuItem2(ID, URI, Label, Selected))

class Banner():
  Text = None
  A = None
  HREF = None
  def __init__(self, *, RenderAlerts, Title = '', TitlePrefix = '', Text = None, A = None, HREF = None):
    self.Title = Title
    self.TitlePrefix = TitlePrefix
    self.Text = Text
    self.A = A
    self.HREF = HREF
    self.RenderAlerts = RenderAlerts
    self.ButtonsLinks = []
    self.RURI = None

  def HTML(self):
    return '''
      <div class="container attributes">
        <div class="row">
          <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12">
              <h5>''' + HS(self.TitlePrefix + WIF(self.Title, ' > ')) + '''</h5>
            </div>
            <div class="col-lg-9 col-md-8 col-sm-6 col-xs-12 postion-alert-section">
              ''' + self.RenderAlerts.HTML() + '''
            </div>
          </div>
        </div>
        <div class="clearfix"></div>
      </div>
      '''

class SideBar():
  def __init__(self, *, Width = None, Menu = None):
    self.Menu = Menu or []
    self.Width = Width or 2

  #def AddMenu(self, *, Label, URI="#", ID=None, Selected=False):
   # self.Menu.append(MenuItem(ID, URI, Label, Selected))

  def AddMenu(self, **args):
    M1 = MenuItem(**args)
    self.Menu.append(M1)
    return M1

  def HTML(self):
    return '''
      <div class="class="col-lg-'''+ HS(self.Width) +''' col-md-'''+ HS(self.Width) +''' col-sm-'''+ HS(self.Width) +''' col-xs-'''+ HS(self.Width) +'''">
        <div class="sidebar-nav">
          <ul class="nav nav-list"> ''' + JN(
            ('''<li class="nav-header">'''+ HS(item.Label) + '''</li> ''' if item.URI == '#' else '''<li class="nav-header"><a href='''+QA(item.URI)+ HS(item.Label) + '''</a></li> ''') 
             + JN('''
            <li><a href=''' + QA(Menu.URI) + '''> ''' + HS(Menu.Label) + '''</a></li>
            ''' for Menu in item.Submenu) for item in self.Menu) + '''
          </ul>
        </div><!--/.well -->
      </div><!--/span-->
      '''

class TopNavBar():
  def __init__(self, *, Menu = None, RightMenu = None, ProjectName = None, BackURI=None, LogoPath = None):
    self.ProjectName = ProjectName or 'Project Name'
    self.Menu = Menu or []
    self.RightMenu = RightMenu
    self.RURI = None
    self.LogoPath = LogoPath
    self.UserName = ''

  def AddMenu(self, **args):
    M1 = MenuItem(**args)
    self.Menu.append(M1)
    return M1

  def AddRightMenu(self, **args):
    self.RightMenu = MenuItem(**args)
    return self.RightMenu

  def HTML(self):
    return '''
    <!-- header starts for the application-->
    <header>
      <div class="navbar navbar-default navbar-static-top">
        <div class="container header-container">
          <div class="navbar-header col-lg-2 col-md-2 col-sm-2 col-xs-12 padding-left-0 padding-right-0">
            <button data-target=".navbar-collapse" data-toggle="collapse" class="navbar-toggle" type="button">
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
              <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">''' + ('''
              <img src=''' +QA(self.LogoPath+ '''?'''+App.CacheTime) +'''> ''' if self.LogoPath else self.ProjectName + ''' <span style="color:white;">Admin</span>
              ''') + '''
            </a>
          </div>
          <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
            ''' + JN((('''
              <li class="dropdown ''' +('''active''' if Menu.Selected  else '')+ '''">
                <a data-toggle="dropdown" class="dropdown-toggle" role="button" href="#" id="drop1">''' + HS(Menu.Label) + ''' <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  ''' + JN('''
                  <li><a href=''' + QA(Menu.URI) + ''' >''' + HS(Menu.Label) + '''</a></li>
                  ''' for Menu in Menu.Submenu) + '''
                </ul>
              </li>
            ''') if len(Menu.Submenu)>0 else ('''
              <li class="''' +('''active''' if Menu.Selected  else '')+ '''">
                <a href='''+ QA(Menu.URI) + '''>''' + HS(Menu.Label) + '''</a>
              </li>
            ''')) for Menu in self.Menu) + '''
            </ul>
            <ul class="nav navbar-nav navbar-right">
              <li class="search-icon">
                <form action="/search" method="get"  style="padding:0px;">
                  <input type="hidden" value=''' + (QA(ML(self.RURI)) if self.RURI else QA("")) + ''' name="RURI"> 
                  <input type="text" class="search-input" placeholder="Search" style="padding:0px;" name="query" value="">
                  <span class="glyphicon glyphicon-search"></span>
                </form>
              </li>
              <li class="dropdown user">
                <a data-toggle="dropdown" class="dropdown-toggle" href="#"> 
                  <img src="/assets/images/user.png"> 
                  ''' + self.UserName + '''
                  <b class="caret"></b>
                </a>
                <ul class="dropdown-menu">
                  ''' + (JN('''
                  <li><a data-href="#" href=''' + QA(Menu.URI) + ''' >''' + HS(Menu.Label) + '''</a></li>
                  ''' for Menu in self.RightMenu.Submenu) if self.RightMenu else '') + '''
                </ul>
              </li>
            </ul>
          </div>
          <!--/.nav-collapse -->
        </div>
      </div>
    </header>'''

###############################################################################
class Footer():
  def __init__(self, *, MenuItems = None, Attribution = None):
    self.Attribution = Attribution or 'Attribution'
    self.MenuItems = MenuItems or []

  def AddMenuItem(self, **args):
    M1 = MenuItem(**args)
    self.MenuItems.append(M1)
    return M1

  def HTML(self):
    return '''
      <!----------  wrapper for footer --------->
    
      <footer id="footer">
        <div class="container">
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <a href="/" class="copyright">''' + self.Attribution+ '''</a>
          </div>
          <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
            <ul class="links">
            ''' + (JN('''
              <li><a href=''' + QA(MenuItem.URI) + '''>''' + HS(MenuItem.Label) + '''</a></li>
              ''' for MenuItem in self.MenuItems) if self.MenuItems else '') + '''
            </ul>
          </div>
        </div>
      </footer>
    '''
###############################################################################
class RenderAlerts():
  def __init__(self, BrowserSession):
    self.BrowserSession = BrowserSession
  def HTML(self):
    Errors = ''
    Infos = ''
    while True:
      v = App.Redis.lpop_str(self.BrowserSession.Errors)
      if v == None:
        break
      Errors += '<li>'+ v +'</li>'
    while True:
      v = App.Redis.lpop_str(self.BrowserSession.Infos)
      if v == None:
        break
      Infos += '<li>'+ v +'</li>'
    return '''<!--error and info message div
      Has to have the same id -->
      <div id='MessageElement' style="text-align:left">
        <div id='AlertErrorElement' class='AlertMsgElement alert alert-danger postion-alert-content' ''' +  ('style="display: none;"' if Errors == '' else 'style="display:block;"') + '''>
          <button aria-hidden="true" data-dismiss="alert" class="close" type="button">×</button>
          <i class="icon-exclamation-sign"></i>&nbsp;Error
          <ul id='AlertErrorList' class='AlertMsgList list-unstyled'>
            ''' + (Errors if Errors else '') + '''
          </ul>
        </div>

        <div id='AlertErrorElement' class='AlertMsgElement alert alert-info postion-alert-content' ''' +  ('style="display: none;"' if Infos == '' else 'style="display:block;"') + '''>
          <button aria-hidden="true" data-dismiss="alert" class="close" type="button">×</button>
          <i class="icon-exclamation-sign"></i>&nbsp;Info
          <ul id='AlertErrorList' class='AlertMsgList list-unstyled'>
            ''' + (Infos if Infos else '') + '''
          </ul>
        </div>
      </div>
      <!-- End of error and info message div -->'''
###############################################################################
class ActionBar():
  def __init__(self):
    self.Body = StringBuilder()

  def AddMenuItem(self, **args):
    M1 = MenuItem(**args)
    self.MenuItems.append(M1)
    return M1

  def HTML(self):
    if self.Body.Value:
      return '''
        <div class="clear-activity-wrapper">
          <div class="row">
            <!----------  wrapper for the content  --------->
            ''' + self.Body.Value + '''
          </div>
        </div>
        '''
    else :
      return ''

###############################################################################
class Primary(LayoutResponse):

  #============================================================================
  def __init__(self, *, Header, BrowserSession):
    # Remember, Header, Status, and Buffer are reserved by the baseclass

    super().__init__(Header=Header)
    
    self.AssetPath = '/AppStruct/UI/CoreAdmin/'
    self.LogoPath = self.AssetPath + 'logo.png?' + App.CacheTime

    self.TitlePrefix = ''
    self.Title = ''
    self.TitleIcon = ''
    self.FooterHTML = ''
    self.Footer = ''
    self.ProjectName = ''
    self.RURI = None
    self.URI = None
    self.ButtonLinks = []
    self.BrowserSession = BrowserSession
    
    self.Error = ErrorList()
    self.Info = InfoList()
    self.LeftSideBar = SideBar()
    self.RightSideBar = SideBar()
    self.TopNavBar = TopNavBar(LogoPath = '/assets/AppCove-Logo-130x35.png?' + App.CacheTime)
    self.Footer = Footer()
    self.CenterWidth = 12;
    self.RenderAlerts = RenderAlerts(self.BrowserSession)
    self.Banner = Banner(RenderAlerts = self.RenderAlerts)
    self.ActionBar = ActionBar()
    
    self.Head = StringBuilder()
    self.Body = StringBuilder()
    self.Tail = StringBuilder()
    self.Script = StringBuilder()
    self.Style = StringBuilder()

    self.CSS = CSSList()
    self.JS = JSList()

    self.Menu = []
    
    def UI_ML(URL, Fragment=Undefined, **kwargs):
      if "RURI" in kwargs:
        url = list(urlsplit(kwargs['RURI']))
        url[3] = urlencode([(q[0],q[1]) for q in parse_qsl(url[3]) if q[0] not in ("EM", "IM")])
        kwargs["RURI"] = urlunsplit(url)
      return ML(URL, _fragment=Fragment, **kwargs)
    self.ML = UI_ML
  #============================================================================

  def AddError(self, E):
    if isinstance(E,str):
      App.Redis.rpush_str(self.BrowserSession.Errors, E)
    elif isinstance(E, ValidationError):
      for ErrorMessage in E.Errors:
        App.Redis.rpush_str(self.BrowserSession.Errors, ErrorMessage.Message)
    elif isinstance(E, BaseException):
      App.Redis.rpush_str(self.BrowserSession.Errors, E.Message)

  #============================================================================

  def AddInfo(self, E):
    if isinstance(E,str):
      App.Redis.rpush_str(self.BrowserSession.Infos, E)
    elif isinstance(E, ValidationError):
      for ErrorMessage in E.Errors:
        App.Redis.rpush_str(self.BrowserSession.Infos, ErrorMessage.Message)
    elif isinstance(E, BaseException):
      App.Redis.rpush_str(self.BrowserSession.Infos, E.Message)

  #============================================================================

  def Process(self):

    self.Tail ('''
      <!-- The Notifier Element. -->  
      <div id="NotifierContainer" class="NotifierContainer" style="top:65px;display:none;">
        <div id="NotifierContent" class="NotifierContent">
        Loading...
        </div>
      </div>
      <!-- End of the Notifier Element. -->
      '''
      )
    self.LeftSideBar.Width = 0
    self.RightSideBar.Width = 0
    if self.LeftSideBar.Width != 0:
      self.CenterWidth -= self.LeftSideBar.Width
    if self.RightSideBar.Width != 0:
      self.CenterWidth -= self.RightSideBar.Width

    self.TopNavBar.ProjectName = self.ProjectName
    self.TopNavBar.RURI = self.RURI or self.URI
    self.Banner.Title = self.Title
    self.Banner.TitlePrefix = self.TitlePrefix
    self.Banner.RURI = self.RURI
    self.Banner.ButtonLinks = self.ButtonLinks
    self.Buffer.write('''
    
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
  
    <title>''' + HS(self.TitlePrefix + WIF(self.Title, ' < ', ' > ')) + '''</title>
  
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" type="text/css">
    <link href="//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" type="text/css">
    <link href="/assets/css/theme.css?''' + App.CacheTime + '''" rel="stylesheet" type="text/css">
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome-ie7.min.css" rel="stylesheet" type="text/css">
    ''' + self.CSS.HTML() + '''
    ''' + WIF(self.Style.Value, '<style>', '</style>') + '''
    ''' + self.Head.Value + '''  
  </head>
  <body>
    <div id="wrap">
    ''' + self.TopNavBar.HTML() + '''
    ''' + self.Banner.HTML() + ('''
      <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
        <div class="row">
          <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 margin-r-20">
            <div style="float: right; margin-top: 10px;" class="btn-group">
              ''' + JN(''' <a href=''' + QA(Link[1]) + ''' class="btn btn-default">''' + HS(Link[0]) +'''</a> ''' for Link in self.ButtonLinks) + (''' 
              <a href=''' + QA(self.RURI) + ''' class="btn btn-success">Go Back</a>''' if self.RURI else '') + '''
            </div>
          </div>
        </div>
      </div>''' if not self.URI.startswith('/account/detail') else '') + '''
      <div class="container">
        <div class="new-position-wrapper">
          ''' + self.ActionBar.HTML() + '''
          <div class="row">
            ''' + (SideBar().HTML() if self.LeftSideBar.Width != 0 else '') + '''
            <div class="col-lg-'''+ HS(self.CenterWidth) +''' col-md-'''+ HS(self.CenterWidth) +''' col-sm-'''+ HS(self.CenterWidth) +''' col-xs-'''+ HS(self.CenterWidth) +'''">
              ''' + self.Body.Value + '''
            </div>
            ''' + (SideBar().HTML() if self.RightSideBar.Width != 0 else '') + '''
            <div id="push"></div>
          </div><!--row-->
        </div><!--new-position-wrapper-->
      </div><!--/.container-->
    </div><!--  wrap -->
    </div>
      ''' + self.Footer.HTML() + '''
        <!-- scripts -->
      <script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js"></script>
      <script src="//code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
      <script src="//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js"></script>
      <script src=''' + QA(self.AssetPath + "Utils.js?" + App.CacheTime) + ''' type="text/javascript"></script>
      ''' + self.JS.HTML() + WIF(self.Script.Value, '<script>', '</script>') + '''
      ''' + self.Tail.Value + '''
    </div>
  </body>
</html>
    ''')


###############################################################################
class Login(LayoutResponse):

  #============================================================================
  def __init__(self, *, Header, BrowserSession):
    # Remember, Header, Status, and Buffer are reserved by the baseclass

    super().__init__(Header=Header)
    
    self.AssetPath = '/AppStruct/UI/CoreAdmin/'
    self.LogoPath = 'assets/CoreAdmin-Logo.png?' + App.CacheTime
#     self.ProjectName = 'PeopleInk'
    self.TitlePrefix = ''
    self.Title = 'Login'
    self.BrowserSession = BrowserSession
    
    self.Error = ErrorList()
    self.Info = InfoList()
    self.Nav1 = SimpleMenu()
    self.Nav2 = SimpleMenu()
    self.RenderAlerts = RenderAlerts(self.BrowserSession)
    self.Footer = Footer()

    self.Head = StringBuilder()
    self.Body = StringBuilder()
    self.Tail = StringBuilder()
    self.Script = StringBuilder()
    self.Style = StringBuilder()
    

    self.CSS = CSSList()
    self.JS = JSList()

    self.Menu = []

    def UI_ML(URL, Fragment=Undefined, **kwargs):
      if "RURI" in kwargs:
        url = list(urlsplit(kwargs['RURI']))
        url[3] = urlencode([(q[0],q[1]) for q in parse_qsl(url[3]) if q[0] not in ("EM", "IM")])
        kwargs["RURI"] = urlunsplit(url)
      return ML(URL, _fragment=Fragment, **kwargs)
    self.ML = UI_ML

  def AddMenu(self, **args):
    M1 = MenuItem(**args)
    self.Menu.append(M1)
    return M1

  #============================================================================

  def AddError(self, E):
    if isinstance(E,str):
      App.Redis.rpush_str(self.BrowserSession.Errors, E)
    elif isinstance(E, BaseException):
      App.Redis.rpush_str(self.BrowserSession.Errors, E.Message)
    elif E.Errors:
      for ErrorMessage in E.Errors:
        App.Redis.rpush_str(self.BrowserSession.Errors, ErrorMessage.Message)

  #============================================================================

  def AddInfo(self, E):
    if isinstance(E,str):
      App.Redis.rpush_str(self.BrowserSession.Infos, E)
    elif isinstance(E, BaseException):
      App.Redis.rpush_str(self.BrowserSession.Infos, E.Message)
    elif E.Errors:
      for ErrorMessage in E.Errors:
        App.Redis.rpush_str(self.BrowserSession.Infos, ErrorMessage.Message)

  #============================================================================
  def Process(self):
    self.JS.Add("//ajax.googleapis.com/ajax/libs/jquery/2.0.2/jquery.min.js")
    #self.JS.Add("//code.jquery.com/ui/1.10.3/jquery-ui.js")
    #self.JS.Add("//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js")
    self.JS.Add(QA(self.AssetPath + "Utils.js?" + App.CacheTime))
    self.Buffer.write('''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="">
  <meta name="author" content="">
  <link rel="shortcut icon" href="/assets/ico/favicon.png?''' + App.CacheTime + '''">

  <title>''' + HS(self.TitlePrefix + WIF(self.Title, ' < ', ' > ')) + '''</title>
  
  <link href="//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css" rel="stylesheet" type="text/css">
  <link href="//code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" type="text/css">
  <link href="/assets/css/theme.css?''' + App.CacheTime + '''" rel="stylesheet" type="text/css">
  <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.min.css" rel="stylesheet" type="text/css">
  <link href="//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome-ie7.min.css" rel="stylesheet" type="text/css">
''' + self.CSS.HTML() + '''
''' + WIF(self.Style.Value, '<style>', '</style>') + '''
</head>
<body>
  <div id="wrap">
    <!-- header starts for the application-->
    <header>
      <div class="login-logo">
        <img class="col-lg-offset-1 col-md-offset-1 col-sm-offset-1" src="/assets/images/logo-login.png"> 
      </div>
    </header>
    <div class="container">
      <div class="row login-content">
        ''' + self.Body.Value + '''
      </div>
    </div>
  </div>
  <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
  <!--[if lt IE 9]>
    <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <script src="//cdnjs.cloudflare.com/ajax/libs/respond.js/1.2.0/respond.js"></script>
  <![endif]-->
  <script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" type="text/javascript"></script>
  <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js" type="text/javascript"></script>
  <script src=''' + QA(self.AssetPath + "Utils.js?" + App.CacheTime) + ''' type="text/javascript"></script>
  ''' + self.JS.HTML() + ''' 
  ''' + WIF(self.Script.Value, '<script>', '</script>') + '''
  ''' + self.Tail.Value + '''
  ''' + self.Footer.HTML() + '''
</body>
</html>
    ''')

