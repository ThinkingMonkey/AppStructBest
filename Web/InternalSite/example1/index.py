# vim:encoding=utf-8:ts=2:sw=2:expandtab

from Project import *


@Expose
def Request(self):
  yield
 
  ItemList = [
    dict(ID=1, Description='Item 1'),
    dict(ID=2, Description='Item 2'),
    dict(ID=3, Description='Item 3'),
    dict(ID=4, Description='Item 4'),
    dict(ID=5, Description='Item 5'),
    ]
  
  
  self.UI.JS.Add('common.js?'+App.CacheTime)
  self.UI.JS.Add('common.css?'+App.CacheTime)

  self.UI.JS.Add('index.js?'+App.CacheTime)
  self.UI.CSS.Add('index.css?'+App.CacheTime)
  
  
  self.UI.Script('''
    $(function(){
      var UI = UIInit(''' + JE(ItemList) + ''');
    });
    ''')

  self.UI.Body('''
    
    <hr />
    <div class="col-md-4">
      <ul id="datalist">
      </ul>

      <form role="form">
        <div class="form-group">
          <input type="text" id="description" placeholder="add new item..."/>
          <input type="submit" value="Add" class="btn" id="addbutton">
        </div>
      </form>
      
      <p>
        To add new item you can use text entry form above or launch <button id="addbutton2">dialog editor</button>
      </p>

      <div class="modal" id="editdialog">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
              <h4 class="modal-title">Modal title</h4>
            </div>
            <div class="modal-body">
              <input type="text" id="editdialog_description" />
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-primary save-button">Save changes</button>
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
      </div><!-- /.modal -->
    </div><!-- div -->

    <div class="col-md-8">
      <p>
      Lorem ipsum dolor sit amet, vix quis adipisci cu, mel duis delectus at. At aeque recusabo eam. Eu quo hinc molestiae deterruisset, cum cetero equidem dolorum ut, omnis ancillae eu mei. Eum id clita facilisis, cu tamquam intellegat liberavisse quo. Eripuit accommodare no has. Ad eos dicit salutatus percipitur.
      </p>
      <p>
      Ei torquatos deterruisset eam. Stet legimus ex sed, ut quod suas suscipit sit. In cum melius fabellas, in latine principes eos. His ut vocibus vivendo suscipit, his eu iriure menandri. Autem quaestio partiendo ut sed, cu mei nemore iracundia. Ut mel nobis graecis abhorreant.
      </p>
      <p>
      Idque evertitur eu mel. Diceret perfecto liberavisse pro an, sit iisque tincidunt in. An malis mundi vix. Vis ut facer concludaturque.
      </p>
      <p>
      Munere necessitatibus vim ex. Mandamus indoctum dissentiunt an mel, at odio audiam ponderum mea. Movet putant eu pri, dicat albucius at eos. Usu omnes graeci et, ad quo modo meliore detraxit. At wisi consectetuer pri, mel illum errem melius ad.
      </p>
      <p>
      In quod congue per, vivendo menandri vix cu. Per electram adversarium et, delectus indoctum ex qui, ne mei suas munere adolescens. Ne sea meliore invidunt, blandit constituam at vim, vix cu aperiri integre. Eos elit detraxit dissentiunt no, has enim principes honestatis an, ad sea maiorum legendos liberavisse. Vim an tota labores partiendo, illum utinam alterum est ad.
      </p>
    </div><!-- div -->


    ''')

  


  
  yield self.UI

