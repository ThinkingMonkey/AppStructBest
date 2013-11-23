/*
vim:encoding=utf-8:ts=2:sw=2:expandtab
*/


//#############################################################################
// We pass all init data to the UI.
function OkCancelDialog() {
  var UI = {};

  var $dialog = $(
    '<div class="modal">'+
    '  <div class="modal-dialog">'+
    '    <div class="modal-content">'+
    '      <div class="modal-header">'+
    '        <h4 class="modal-title"></h4>'+
    '      </div>'+
    '      <div class="modal-body">'+
    '      </div>'+
    '      <div class="modal-footer">'+
    '        <button type="button" class="btn btn-primary save-button">Ok</button>'+
    '        <button type="button" class="btn btn-default cancel-button">Cancel</button>'+
    '      </div>'+
    '    </div><!-- /.modal-content -->'+
    '  </div><!-- /.modal-dialog -->'+
    '</div><!-- /.modal -->'
  ).filter('.modal');  //This is required because the jQuery object will create a modeal for the <div> and <!-- comment
   
  UI.$dialog = $dialog;

  var $title = $dialog.find('.modal-title');
  var $body = $dialog.find('.modal-body');
  var $savebutton = $dialog.find('.save-button');
  var $cancelbutton = $dialog.find('.cancel-button');

  var onClose = null;

//  $dialog.modal({show: false, backdrop: 'static'});
  
  // onClose will accept a boolean (ok = true, cancel = false)
  UI.show = function(title, message, onCloseFunction) {
    onClose = onCloseFunction;
    $title.text(title);
    $body.text(message);
    $dialog.modal('show');
  };

  $savebutton.click(function(evt){
    evt.preventDefault();
    $dialog.modal('hide');
    if(onClose)
      onClose(true);
    onClose = null;
  });
  
  $cancelbutton.click(function(evt){
    evt.preventDefault();
    $dialog.modal('hide');
    if(onClose)
      onClose(false);
    onClose = null;
  });

  return UI;
};

