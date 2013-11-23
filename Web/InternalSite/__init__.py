# vim:encoding=utf-8:ts=2:sw=2:expandtab

from Project import *

import AppStruct.Web.Handler.Point
import AppStruct.Web.Plugin
import Project.UI.Admin


###############################################################################
class application(
  AppStruct.Web.Handler.Point.PointHandler,
  AppStruct.Web.Plugin.QueryString,
  AppStruct.Web.Plugin.Post,
  AppStruct.Web.Plugin.SessionToken,
  AppStruct.Web.Plugin.Cookie,
  AppStruct.Web.Plugin.Logger,
  ):

  ScriptPathMatch = '/'

  # Instance variables
  UI = None
  Admin = None

  # Instance Settings
  Auth_Required = True
  Perm_Usage_Required = True
  Perm_Active_Required = True
  Perm_Admin_Required = False

  # Session Support
  BrowserSession = None  # This is bound to a session token
  AdminSession = None  # This is bound to a user + session token (crosses logins from same browser and user)
  AdminData = None  # This is bound to a user (crosses computers for same user)

  # Misc Nginx Communication
  ProxySSL = None
  ProxyHost = None

  # Set to 'http' to force http, 'https' to force https, or None to accept either.
  RequireProtocol = 'https'

  # Beginning of Request handler
  def RequestStart(self):
    App.Open(Logger = self.Log)
    self.BrowserSession = SessionKey('BrowserSession', self.SessionToken)

    App.Log(self.Env)

    # FYI: Nginx or mod_wsgi adds HTTP_ to the beginning of env variables set with proxy_set_header

    if 'HTTP_SCHEME' not in self.Env:
      raise Exception('Cannot run application without Scheme environment variable set')
    elif self.Env['HTTP_SCHEME'] == 'http':
      self.ProxySSL = False
    elif self.Env['HTTP_SCHEME'] == 'https':
      self.ProxySSL = True
    else:
      raise Exception("Cannot run application without Scheme environment variable set to either 'http' or 'https' instead of: {0}".format(self.Env['HTTP_Scheme']))

    if 'HTTP_HOST' in self.Env:
      self.ProxyHost = self.Env['HTTP_HOST']
    else:
      raise Exception('Cannot run application without Host environment variable set')

    App.Log('Start Request To: ' + ('https://' if self.ProxySSL else 'http://') + self.ProxyHost + self.Env.URI)

  # End of Request handler
  def RequestEnd(self, res, exc):
    App.Close()

###############################################################################

@Expose
def Init(self):
  yield

  App.Log('Session Token is ' + str(self.SessionToken))


  # ---------------------------------------------------------------------------
  # Establish public site layout

  self.UI = self.Response(Project.UI.Admin.Primary, BrowserSession = self.BrowserSession)
  self.UI.TitlePrefix = 'AppStructBest'
  self.UI.ProjectName = 'AppStructBest'
  self.UI.URI = self.Env.URI
  
  #----------------------------------------------------------------------------
  yield

@Expose
def Mapper(self, parts):
  if parts == ('logout',):
    return Logout

@Expose
def Logout(self):
  App.Redis.delete(self.BrowserSession.Admin_MNID)
  self.UI = self.Response(Project.UI.Admin.Login, BrowserSession = self.BrowserSession)
  self.UI.AddInfo('Logout successful')
  yield self.RedirectResponse(ML('/login'))
  yield

