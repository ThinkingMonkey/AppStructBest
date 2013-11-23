# vim:encoding=utf-8:ts=2:sw=2:expandtab

from Project import *
import re


IS_IDENTIFIER = re.compile('^[a-zA-Z_][a-zA-Z0-9_]*$').match


def MakeSIUD(Schema, Table, *primarykeys):

  if len(primarykeys) == 0:
    raise TypeError('Must pass at least one primary key argument')

  if not IS_IDENTIFIER(Schema):
    raise ValueError('Invalid schema: {0}'.format(Schema))
    
  if not IS_IDENTIFIER(Table):
    raise ValueError('Invalid table: {0}'.format(Table))

  sqlTable = '"{0}"."{1}"'.format(Schema, Table)
  sqlWhere = ''
  sqlPrimaryFields = ''

  for i,k in enumerate(primarykeys):
    if not IS_IDENTIFIER(k):
      raise ValueError('Invalid primary key field: {0}'.format(k))

    sqlWhere += 'AND "{0}" = $PK_{1}\n'.format(k, i)
    sqlPrimaryFields += '"{0}", '.format(k)

  sqlPrimaryFields = sqlPrimaryFields[:-2]  #strip comma space


  #============================================================================
  def SELECT(self, fields):
    kwargs = dict((('PK_{0}'.format(i),v) for i,v in enumerate(self.PrimaryKey)))
    return App.DB.Row('''
      SELECT
        [Field] 
      FROM 
        ''' + sqlTable + '''
      WHERE True 
        ''' + sqlWhere + '''
      ''',
      *fields,
      **kwargs
      )
  
  def INSERT(self, data):
    return App.DB.TRow('''
      INSERT INTO 
        ''' + sqlTable + '''
        ([Field])
      VALUES
        ([Value])
      RETURNING
        ''' + sqlPrimaryFields + '''
      ''',
      *data.items()
      )

  def UPDATE(self, data):
    kwargs = dict((('PK_{0}'.format(i),v) for i,v in enumerate(self.PrimaryKey)))
    App.DB.Execute('''
      UPDATE 
        ''' + sqlTable + '''
      SET
        [Field=Value]
      WHERE True
        ''' + sqlWhere + '''
      ''',
      *data.items(),
      **kwargs
      )
  
  def DELETE(self):
    kwargs = dict((('PK_{0}'.format(i),v) for i,v in enumerate(self.PrimaryKey)))
    App.DB.Execute('''
      DELETE FROM  
        ''' + sqlTable + '''
      WHERE True
        ''' + sqlWhere + '''
      ''',
      **kwargs
      )

  return SELECT, INSERT, UPDATE, DELETE

