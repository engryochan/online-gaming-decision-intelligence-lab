/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/themes/custom/euronext_base/js/util.js. */
window.dataLayer = window.dataLayer || [];
//535
jQuery('span.file--mime-application-xml a').attr('download',"");


// Page load
jQuery(document).ready(function() {

  var t = bootstrap.Tooltip.Default.whiteList;
  t.li.push('onclick');

  var initBsTooltip = function(){
    once('bstooltipinit','[data-bs-toggle="tooltip"]').forEach(function(element){
      new bootstrap.Tooltip(element);
    });
  };

  initBsTooltip();

  jQuery(document).ajaxComplete(function(event, xhr, settings) {
    initBsTooltip();
  });

  if ( drupalSettings.user.uid != 0 ){
    if (window.parent) {
      parent.postMessage('connected::true','*');
    }
  }

	//Tips to correct dropdown first click
	jQuery(".navbar div[data-toggle=\"dropdown\"]").each(function() {
    if (jQuery(this).html()) {
		  jQuery(this).trigger("click");
    }
	});

    //trick to display SVG with url in IE
	svg4everybody();
    // for jira 139
    if(drupalSettings.custom && drupalSettings.custom.asset_files_path){
      jQuery('.platform-down-right-arrow').html('<svg width="16" height="16" class="d-block"><use xlink:href="'+drupalSettings.custom.asset_files_path+'/spritemap.svg#down-right-arrow"></use></svg>');
    }
    jQuery('.platform-down-right-arrow').parent().prev().css('order','2');

    //define startsWith for IE
    if (!String.prototype.startsWith) {
       String.prototype.startsWith = function(searchString, position){
         return this.substr(position || 0, searchString.length) === searchString;
      };
    }

   if (isIE()) { jQuery(".dropdown__vanilla").removeClass("dropdown__vanilla"); }

  // method to automatically append the sort arrows in <th>
  var addSortArrowToTh = function(){
    jQuery('th:not(:empty):not(:has(span.sort-arrows))').append('<span class="sort-arrows"></span>');
  }
  jQuery('body').on( 'draw.dt', 'table', function(){
    addSortArrowToTh();
  });
});

//method to get form elements as object
jQuery.fn.serializeObject = function() {
  var obj = {};
  jQuery.each(this.serializeArray(), function(i, o) {
    var n = o.name,
      v = o.value;
    obj[n] = obj[n] === undefined ? v :
      jQuery.isArray(obj[n]) ? obj[n].concat(v) : [obj[n], v];
  });
  return obj;
};

//method to sort "dd/mm/yyyy" correctly in datatable
jQuery.extend(jQuery.fn.dataTableExt.oSort, {
    "extract-date-pre": function(value) {
        var date = jQuery(value, 'span')[0].innerHTML;
        date = date.split('/');
        return Date.parse(date[1] + '/' + date[0] + '/' + date[2])
    },
    "extract-date-asc": function(a, b) {
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },
    "extract-date-desc": function(a, b) {
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});

function isIE() {
        var ua = window.navigator.userAgent;
        return /MSIE|Trident/.test(ua);
}


function get_datatable_current_order(tableid, default_sort){
  var final_order = [];
  var table = null;
  if (jQuery.fn.DataTable.isDataTable(tableid) ) {
    table = jQuery(tableid).DataTable();
  }

  if(table != null) {
    if(table.settings().order().length > 0) {
      var order_table = [];
      var currentTableOrder = table.settings().order()[0];
      order_table.push(currentTableOrder[0]);
      order_table.push(currentTableOrder[1]);
      final_order.push(order_table);
    }
  }
  else if(default_sort != null)
    final_order.push(default_sort);

  return final_order;
}

function add_datatable_export_buttons(table, filename, withTextDescription, withprint, additionalHeader, customizeHeaderExport, no_dl,ms_top) {
  var mybuttons = [];

var tt = undefined;
   if ( jQuery('#'+table['context'][0]['sTableId']).parents('div.card').find('div.card-header h3').text() != "" )
   {
        tt =  jQuery('#'+table['context'][0]['sTableId']).parents('div.card').find('div.card-header h3').text();
    }
   else{

         tt = jQuery('#'+table['context'][0]['sTableId']).parents('div.modal').find('h2').text();
   }




  if(withprint == true || withprint == null) {
     var print_button_options = {
      extend: 'print',
      className:'btn btn-link d-flex align-items-center pr-0',
      text : '<div class="svg_container"> <svg viewBox="0 0 24 24" width="24" height="24" role="presentation"><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#print"></use></svg> </div>',
      footer: true,
      title: filename.replace('_', ' ').replace('_', ' '),
            init: function( api, node, config) {
                jQuery(node).removeClass('dt-button')
            },
      customize: function ( win ) {

        if (additionalHeader != null && additionalHeader != '')
          jQuery(win.document.body).find( 'thead' ).prepend(additionalHeader);


              jQuery(win.document.body)
                  .css( 'font-size', '10pt' )
                  .prepend(
                      '<img src="https://connect2.euronext.com/themes/custom/euronextd8/logo.svg" style="top:0;left:0;width:220px;" />'
                  );
  jQuery(win.document.body).find( 'table' ).css('font-family','Inter-regular,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji" ');
 jQuery(win.document.body).find( 'h1,h2,h3' ).css('font-family','Inter-regular,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji" ');

              jQuery(win.document.body).find( 'table' ).css( 'width' , '100%' );


                if (  table['context'][0]['sTableId'].includes('Watchlist')){

                   jQuery(win.document.body).find('table tbody td:nth-child(1)').css('text-align', 'left');
                   jQuery(win.document.body).find('table thead th:nth-child(1)').css('text-align', 'left');

              jQuery(win.document.body).find('table thead th:nth-child(2),table thead th:nth-child(3),table thead th:nth-child(4),table thead th:nth-child(5),table thead th:nth-child(6),table thead th:nth-child(7),table thead th:nth-child(8),table thead th:nth-child(9)' ).css( 'text-align' , 'center' );
              jQuery(win.document.body).find('table tbody td:nth-child(2),table tbody td:nth-child(3),table tbody td:nth-child(4),table tbody td:nth-child(5),table tbody td:nth-child(6),table tbody td:nth-child(7),table tbody td:nth-child(8),table tbody td:nth-child(9)' ).css( 'text-align' , 'center' );
                   }
            else{
              jQuery(win.document.body).find( 'td' ).css( 'text-align' , 'center' );
              jQuery(win.document.body).find( 'th' ).css( 'text-align' , 'center' );
             }

                        var title ="";
                jQuery.map(jQuery(table.table().container()).parents('div.modal').find('.modal-title span,.modal-title h2,.modal-title h3'), function (el, i) {
                        if (i==0) { title += jQuery(el).text() + " - " ;}else{ title += jQuery(el).text(); }
                });

                 var tt =  jQuery('#'+table['context'][0]['sTableId']).parents('div.card-body div.py-0>div').attr('id');

               dataLayer.push({
                'event' : 'generic',
                'e_category' : 'print',
                'e_action': title,
                'e_label':  window.location.href +'-'+tt
                });

          }
    }
    if (withTextDescription) { print_button_options.text += Drupal.t("Print"); }
    mybuttons.push(print_button_options);
  }

  if (no_dl == true || no_dl == null ){

   var excel_button_options = {
            extend: 'excel',
            messageTop: ms_top,
        className: 'btn btn-link d-flex align-items-center pr-0',
        text: '<div class="svg_container"> <svg viewBox="0 0 24 24" width="24" height="24" role="presentation" class="download"><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#download"></use></svg></div>',
            footer: true,
            filename: filename,
            title: filename.replace('_', ' ').replace('_', ' '),
                    exportOptions: {
                       format: {
                           body: function(data, row, column, node) {
                              data = jQuery('<p>' + data + '</p>').text();
                              var dataTemp = data.replace(' ','');
                                 if (jQuery.isNumeric(dataTemp.replace(',', '.')) && ( drupalSettings.path.currentLanguage != 'en')) {
                                    return dataTemp.replace(',', '.');
                                 }

                               return data;
                           }
                       }
                   },
                customize: function( xlsx ) {

         dataLayer.push({
        'event' : 'generic',
        'e_category' : 'fonctionnality file',
        'e_action': filename,
        'e_label':  window.location.href +'-'+ tt
        });
        },
       init: function( api, node, config) {
          jQuery(node).removeClass('dt-button')
      }
  };
  if (withTextDescription) { excel_button_options.text += Drupal.t("Download"); }


    if(additionalHeader == true) {
            excel_button_options.exportOptions.format.header = function (data, columnIdx) {console.info(customizeHeaderExport);
              if (customizeHeaderExport != null && customizeHeaderExport[columnIdx] != null) {return customizeHeaderExport[columnIdx];}
          }
    }
    mybuttons.push(excel_button_options);
 }

  new jQuery.fn.dataTable.Buttons( table, {
      buttons: mybuttons
  } );
  return table;

}

function add_datatable_colvis_buttons(table, column_list) {
    if(column_list == null) column_list = '';

    new jQuery.fn.dataTable.Buttons( table, {
        'buttons': [  {
            extend: 'colvis',
            columns: column_list,
            text: Drupal.t('Active Columns'),
            action: function (e, dt, node, config) {
                var temp = jQuery.fn.dataTable.ext.buttons.collection.action;
                temp(e, dt, node, config);
                jQuery('div.dt-buttons').addBack('d-flex align-items-center');
                jQuery('div.dt-button-collection').addClass('checkbox-dropdown');
            }

        },
        ]
    } );
    return table;
}
function graphExport(chart,format,filename)
{
  var is_print = false;
  switch(format){
    case 'csv':
        chart.export.capture({}, function() {
          this.toCSV({}, function (data) {
              this.download(data, this.defaults.formats.CSV.mimeType, filename);
          });
        });
    break;
    case 'json':
        chart.export.capture({}, function() {
          this.toJSON({}, function (data) {
            this.download(data, this.defaults.formats.JSON.mimeType,filename);
          });
        });
    break;
    case 'png':
        chart.export.capture({}, function() {
          this.toPNG({}, function (data) {
            this.download(data, this.defaults.formats.PNG.mimeType, filename);
          });
        });
    break;
    case 'svg':
        chart.export.capture({}, function() {
            this.toSVG({}, function (data) {
                this.download(data, this.defaults.formats.SVG.mimeType, filename);
            });
        });
    break;
    case 'pdf':
        chart.export.capture({}, function() {
            this.toPDF({}, function (data) {
                this.download(data, this.defaults.formats.PDF.mimeType, filename);
            });
        });
    break;
    case 'jpg':
        chart.export.capture({}, function() {
            this.toJPG({}, function (data) {
                this.download(data, this.defaults.formats.JPG.mimeType, filename);
            });
        });
    break;
    case 'xlsx':
        chart.export.capture({}, function() {
            this.toXLSX({}, function (data) {
                this.download(data, this.defaults.formats.XLSX.mimeType, filename);
            });
        });
    break;
    case 'print':
        chart.export.capture({}, function () {
            this.toPRINT();
        });
        is_print = true;
    break;

  }

  var tt = undefined;

          if ( jQuery('#'+chart.div.id).parents('div.card').find('div.card-header h3').text() != "" )
   {
        tt =  jQuery('#'+chart.div.id).parents('div.card').find('div.card-header h3').text();
    }
   else if ( jQuery('#'+chart.div.id).parents('div.modal').find('h2').text() != "" ){

         tt = jQuery('#'+chart.div.id).parents('div.modal').find('h2').text();
   }
   else {
        tt= Drupal.t("Chart");
        }


   if ( is_print === false){
     dataLayer.push({
        'event' : 'generic',
        'e_category' : 'fonctionnality file',
        'e_action': filename,
        'e_label':  window.location.href +'-'+tt
        });
   }
  else{

             dataLayer.push({
        'event' : 'generic',
        'e_category' : 'print',
        'e_action': filename,
        'e_label':  window.location.href +'-'+tt
        });



   }



  if(jQuery(".popover").length) jQuery(".popover").popover('hide');
}

function getAllUrlParams(url) {

  // get query string from url (optional) or window
  var queryString = url ? url.split('?')[1] : window.location.search.slice(1);

  // we'll store the parameters here
  var obj = {};

  // if query string exists
  if (queryString) {

    // stuff after # is not part of query string, so get rid of it
    queryString = queryString.split('#')[0];

    // split our query string into its component parts
    var arr = queryString.split('&');

    for (var i = 0; i < arr.length; i++) {
      // separate the keys and the values
      var a = arr[i].split('=');

      // set parameter name and value (use 'true' if empty)
      var paramName = a[0];
      var paramValue = typeof (a[1]) === 'undefined' ? true : a[1];

      // (optional) keep case consistent
      paramName = paramName.toLowerCase();
      if (typeof paramValue === 'string') paramValue = paramValue.toLowerCase();

      // if the paramName ends with square brackets, e.g. colors[] or colors[2]
      if (paramName.match(/\[(\d+)?\]$/)) {

        // create key if it doesn't exist
        var key = paramName.replace(/\[(\d+)?\]/, '');
        if (!obj[key]) obj[key] = [];


        // if it's an indexed array e.g. colors[2]
        if (paramName.match(/\[\d+\]$/)) {
          // get the index value and add the entry at the appropriate position
          var index = /\[(\d+)\]/.exec(paramName)[1];
          obj[key][index] = paramValue;
        } else {
          // otherwise add the value to the end of the array
          obj[key].push(paramValue);
        }
      } else {
        // we're dealing with a string
        if (!obj[paramName]) {
          // if it doesn't exist, create property
          obj[paramName] = paramValue;
        } else if (obj[paramName] && typeof obj[paramName] === 'string'){
          // if property does exist and it's a string, convert it to an array
          obj[paramName] = [obj[paramName]];
          obj[paramName].push(paramValue);
        } else {
          // otherwise add the property
          obj[paramName].push(paramValue);
        }
      }
    }
  }

  return obj;
}

jQuery('body').on('click', function (e) {
  add_modal_basic_event();
  jQuery('[data-toggle="popover"]').each(function () {
    //the 'is' for buttons that trigger popups
    //the 'has' for icons within a button that triggers a popup
    if (!jQuery(this).is(e.target) && jQuery(this).has(e.target).length === 0 && jQuery('.popover').has(e.target).length === 0) {
      jQuery(this).popover('hide');
    }
  });
});


 if(window.location.href.indexOf("cas/logout") > -1) {
  var new_url = getAllUrlParams(window.location.href).url.replace('%3a',':');
  window.location.href = new_url;
 }

(function($, Drupal, drupalSettings) {
  Drupal.behaviors.AFCfileError = {
    attach: function (context, settings) {
      jQuery(once('checkdomchange', '.form-managed-file')).bind("DOMSubtreeModified", function(){
        var msgs = jQuery(this).find('.messages');
        if(msgs.length>0){
          msgs.detach().appendTo(jQuery(this).parent());
          jQuery(this).css('overflow','hidden');
          if(!jQuery('.messages--error').hasClass('alert')){
            jQuery('.messages--error').css('margin-top','1rem');
            jQuery('.messages--error').prepend('<svg viewBox="0 0 24 24" width="24" height="24" class=""><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#alert"></use></svg>');
            jQuery('.messages--error').append('<button type="button" class="close" data-dismiss="alert" aria-label="Close"><svg viewBox="0 0 24 24" width="24" height="24" class=""><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#close-notification"></use></svg></button>');
            jQuery('.messages--error').addClass('alert alert-danger text-white  alert-dismissible fade show  mb-3');
            jQuery('.messages--error').attr('role','alert');
          }
        }
      });
    }
  };

  Drupal.behaviors.twitterSlick = {
    attach: function(context, settings) {
      if ($( ".block-twitter-api-block-search .item-list ul, .block-enx-twitter-cards .item-list ul, .paragraph--type--twitter-links .field--type-entity-reference").length > 0) {
        $('.block-twitter-api-block-search .item-list ul, .block-enx-twitter-cards .item-list ul, .paragraph--type--twitter-links .field--type-entity-reference').slick({
          "prevArrow": '<button type="button" data-role="none" class="slick-prev enx-slick-prev slick-arrow" aria-label="Previous" style="">Previous</button>',
          "nextArrow": '<button type="button" data-role="none" class="slick-next enx-slick-next slick-arrow" aria-label="Next" style="">Next</button>',
          "dots": false,
          "infinite": false,
          "speed": 300,
          "slidesToShow": 3,
          "slidesToScroll": 3,
          "accessibility": true,
          "swipe": true,
          "swipeToSlide":true,
          "draggable": true,
          "responsive":[
            {"breakpoint":480,"settings":{"slidesToShow":1,"slidesToScroll": 1,"swipeToSlide":true}},
            {"breakpoint":900,"settings":{"slidesToShow":2,"slidesToScroll": 2,"swipeToSlide":true}},
          ]
        });
      }
    },
  };

})(jQuery, Drupal, drupalSettings);

/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/themes/custom/euronext_base/js/util.js. */