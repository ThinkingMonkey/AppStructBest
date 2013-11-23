/*
vim:encoding=utf-8:ts=2:sw=2:expandtab
*/



// //#############################################################################
// // We pass all init data to the UI.
// function UIInit(ItemList) {
//   var UI = {};
// 
//   // This represents a specific part of the UI
//   UI.Listing = function(){
//
//     // private methods/vars/etc...
// 
//     return {public interface};
//   }();
// 
//   
//   // This is the dialog.
//   UI.DialogEditor = function(){
//
//     // private methods/vars/etc...
// 
//     return {public interface};    
//   }();
// 
// 
//   //===========================================================================
//   //Init code goes here after we have UI.Listing and UI.DialogEditor.
//   if(! $.isArray(ItemList))
//     throw {Type: 'ValueError', Description: 'Missing ItemList argument'};
// 
// 
//   return UI;
// }


var AppStruct = {};

AppStruct.ValidationError = function(ErrorList){
  exc = {};
  exc.Type = 'ValidationError';
  exc.ErrorList = ErrorList;

  exc.Messages = function() {
    data = '';
    $.each(ErrorList, function(k,v){
      data += v.Message + "\n";
    });
    return data;
  }  
  return exc;
};



//#############################################################################
// We pass all init data to the UI.
function UIInit(ItemList) {
  var UI = {};

  //===========================================================================
  // Pull this in from the common.js library
  UI.OkCancelDialog = OkCancelDialog();
  
  //===========================================================================
  function ItemClass(data) {
    var ItemObject = {};
    
    ItemObject.onUpdate = null;
    
    function Validate(data) {
      var EL = [];
      
      if(! data.Description) 
        EL.push({ID: 'Description', Message: 'Description is required'});

      if(EL.length > 0)
        throw AppStruct.ValidationError(EL);
    };

    ItemObject.Update = function(data) {
      Validate(data);
      ItemObject.Description = data.Description;
      
      if(ItemObject.onUpdate) {
        ItemObject.onUpdate();
      }
    };

    // If no params passed, then create a new empty object
    if(! data) {
      ItemObject.ID = 101;
      ItemObject.Description = '';
    }
    else {
      Validate(data);
      ItemObject.ID = data.ID;
      ItemObject.Description = data.Description;
    }
   
    return ItemObject;
  };


  //===========================================================================
  // This represents a specific part of the UI
  UI.ListButtons = function(){
    var $description = $('#description');
    var $addbutton = $('#addbutton');
    var $addbutton2 = $('#addbutton2');
  
    $addbutton.click(function(evt){
      evt.preventDefault();
      try {
        var item = ItemClass({ID: 100, Description: $description.val()});
        UI.Listing.CreateItem(item);
        $description.val('');
        $description.focus();
      } 
      catch(ex) {
        if(ex.Type === 'ValidationError')
          alert(ex.Messages());
        else
          throw(ex);
      }
    });


    $addbutton2.click(function(evt){
      evt.preventDefault();
      
      var item = ItemClass();
      
      UI.DialogEditor.show(item, function(){
        UI.Listing.CreateItem(item);      
      });
    });


    return {};
  }();
  
  
  //===========================================================================
  // This represents a specific part of the UI
  UI.Listing = function(){
    // --------------------------------------------------------------------------
    // Obtain references to all DOM elements that need modified.  Use $ as prefix if jQuery object
    var $datalist = $('#datalist');

    // --------------------------------------------------------------------------
    // Create functions for interactions
    function CreateItem(Item) {
      var listItem = {};
      
      listItem.Item = Item;

      listItem.$element = $(
        '<li>'+
        ' <span></span>'+
        ' <a class="edit" href="#">edit</a>'+
        ' <a class="remove" href="#">remove</a>'+
        '</li>'
        );

      listItem.$element.find('a.edit').click(function(evt){
        evt.preventDefault();
        UI.DialogEditor.show(listItem.Item);
      });
    
      listItem.$element.find('a.remove').click(function(evt){
        evt.preventDefault();
        UI.OkCancelDialog.show('Are you sure?', 'do you really want to?', function(ok){
          if(ok) 
            RemoveItem(listItem);
        });
      });
      
      listItem.Item.onUpdate = function() {
        listItem.$element.find('span').text(listItem.Item.Description); 
      };
     
      // Must update our own DOM when creating self
      listItem.Item.onUpdate();

      $datalist.append(listItem.$element);

      return listItem;
    }

    // Accept a reference of the item
    function RemoveItem(listItem) {
      listItem.$element.remove();
      alert('Removed Item ' + listItem.Item.ID);
    }

    // Public interfaces
  	return {
  	  CreateItem: CreateItem
  	}
  }();

  //===========================================================================
  // This is the dialog.
  UI.DialogEditor = function(){
    
    var $dialogEl = $('#editdialog');
    var $descriptionEl = $('#editdialog_description');

    // Represents Item being edited in dialog
    var currentItem = null;
    var successCallback = null;

    // Main interface to show the dialog ready to edit.
    function show(ItemObject, onSuccess) { 
      currentItem = ItemObject;
      successCallback = onSuccess;

      $descriptionEl.val(currentItem.Description);
      $dialogEl.modal({show:true});
      $descriptionEl.focus();
    };

    
    $dialogEl.find('.save-button').click(function(e) {
      e.preventDefault();
      
      data = {
        Description: $descriptionEl.val()
      };
      
      try {
        currentItem.Update(data);
        $dialogEl.modal('hide');
      }
      catch(ex) {
        if(ex.Type === 'ValidationError') {
          alert(ex.Messages());
          return;
        }
        else {
          throw(ex);
        }
      }
      
      if (successCallback) {
        successCallback(currentItem);
      }
    });


    // Public interfaces
  	return {
  	  show: show
  	}
  }();


  //===========================================================================
  //Init code goes here after we have UI.Listing and UI.DialogEditor.
  if(! $.isArray(ItemList))
    throw {Type: 'ValueError', Description: 'Missing ItemList argument'};
    
  // Initialize screen.  Load data if present
  $.each(ItemList, function(k,data) {
    var item = ItemClass(data);
    UI.Listing.CreateItem(item);
  });


  return UI;
}



