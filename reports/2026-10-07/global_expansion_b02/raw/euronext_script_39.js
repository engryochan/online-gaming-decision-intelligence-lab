/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/modules/custom/awl_product_directory_es/js/awl-pd-es.js. */
var pd_datatables;
var sortname_index = 0;
let initialLetter = 'initialLetter';
(function ($, Drupal, drupalSettings) {
  var data_filters = {};
  var awl_pd_has_filter_trigger_click = false;
  var s = 0;
  var _sZeroRecords;
  // Change the title of the tab with the title of the header
  window.parent.document.title = jQuery(".page-header h1.title").text();
  var checkTri = 0;
  var type = drupalSettings.type;
  var displayLength = 100;
  var alphabetSearchTriggered = false;
  let filterSearchTriggeredAtLeastOnce = false;
  var columnsClasses = [];
  for (var i = 0; i < drupalSettings.datapoints.length; i++) {
    var className = type + '-' + drupalSettings.datapoints[i];
    if (drupalSettings.datapoints[i] == 'name' || drupalSettings.datapoints[i] == 'fullInstrumentName') {
      sortname_index = i;
      //use SMD shortname field to sort by name
      if (drupalSettings.datapoints[i] == 'name') {
        className = type + "-shortName";
      }
      //use SMD name field to sort by fullInstrumentName
      if (drupalSettings.datapoints[i] == 'fullInstrumentName') {
        className = type + "-name";
        initialLetter = 'initialLetterLong';
      }
    }
    columnsClasses.push({ className: className });
  }
  Drupal.behaviors.awl_pd_datas_es = {
    attach: function (context, settings) {
      let url = new URL(window.location.href);
      let pageNumber = parseInt(url.searchParams.get('page'));
      startPage = (!Number.isNaN(pageNumber) && pageNumber >= 0) ? pageNumber * displayLength : 0;
      $(once('pd-datatables', '#stocks-data-table-es')).each(function () {
        _sZeroRecords = Drupal.t('<div>Your search yielded no results <ul><li><span>Check if your spelling is correct.</span></li><li><span>Remove quotes around phrases to match each world individually: "blue smurf" will match less than blue smurf.</span></li><li><span>Consider changing filters</span></li></ul></div>');
        var _sError = Drupal.t('<strong>This data item is currently unavailable. Please try again later.</strong>');
        pd_datatables = $("#stocks-data-table-es").DataTable({
          "bLengthChange": false,
          "bPaginate": true,
          "responsive": {
            'details': false
          },
          "autoWidth": false,
          "bProcessing": true,
          "displayStart": startPage,
          "bServerSide": true,
          'language': {
            'emptyTable': 'Content unavailable',
            'thousands': ' '
          },
          "iDisplayLength": displayLength,
          "ordering": true,
          "pagingType": "simple_numbers",
          "sDom": '<"top"iHB>r<"links">t<"bottom"lp><"clear">',
          "ajax": {
            type: "POST",
            url: drupalSettings.jsongateway,
            dataType: "json",
            data: function (d) {
              if (typeof data_filters.args != "undefined") {
                $.extend(d, data_filters);
              }
              if (!d.args) {
                d.args = {};
              }
              d.args['display_datapoints'] = drupalSettings.datapoints.join(',');
              d.iDisplayLength = d.length;
              d.iDisplayStart = s = d.start;
              //warrt
              if (type == 'warrt' || type == 'funds') {
                //multiSorting
                if (d.order[0] != undefined && d.order[1] != undefined) {
                  d.sSortDir_0 = "";//d.order[0].dir+","+d.order[1].dir;//asc,asc
                  d.sSortField = "";//columnsClasses[d.order[1].column].className.split("-").pop()+","+columnsClasses[d.order[0].column].className.split("-").pop();   //symbol,underlyingInstrument
                }
                else {
                  if (d.draw > 2) {
                    d.sSortDir_0 = d.order[0].dir;
                    d.sSortField = columnsClasses[d.order[0].column].className.split("-").pop();
                  }
                }
              }
              else {
                d.sSortDir_0 = d.order[0].dir;
                d.sSortField = columnsClasses[sortname_index].className.split("-").pop();
              }
              d;
            },
            complete: function () {
              jQuery('[data-toggle="popover"]').popover();
            },
          },
          "initComplete": function (settings, data) {
            settings.oLanguage.sZeroRecords = (typeof data.error != "undefined" && data.error == true) ? _sError : _sZeroRecords;
            $('#stocks-data-table-es').attr('style', '');
            jQuery("#content > section div.block.block-awl-product-directory-es.block-awl-pd-datas-es-block > div.customLoading").remove();
            $("#div-stocks-data-table-es").show();
            $(".dt-buttons").addClass("d-flex align-items-center");
            // $("[data-datapoints=\"name\"]").attr("style", "width: 185px!important");
          },
          alphabetSearch: {
            column: (type == 'stocks' || (type == 'tracker' && $.inArray('name', drupalSettings.datapoints) == "-1")) ? 1 : 0
          },
          buttons: [{
            text: '<span class="text-xs text-dark">' + Drupal.t("Help") + '</span><div class="svg_container"><svg viewBox="0 0 24 24" width="24" height="24"><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#info"></use></svg></div>',
            className: "btn btn-link text-decoration-none d-flex align-items-center",
            attr: {
              "data-toggle": "popover",
              "data-placement": "top",
              "data-html": "true",
              "data-content": drupalSettings.help_text,
              "data-original-title": "",
              "title": "",
              "id": "HelpButtonPD"
            },
            init: function (api, node, config) {
              $(node).removeClass("dt-button");
              $(node).find("> span").contents().unwrap();
              $(node).popover();
            },
          },
          {
            text: '<svg viewBox="0 0 24 24" width="24" height="24"><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#download"></use></svg>',
            className: "btn btn-link",
            init: function (api, node, config) {
              $(node).removeClass("dt-button");
            },
            action: function (e) {
              $("#downloadModal").remove();
              var modal = "";
              modal +=
                "<div class=\"modal fade modals\" id=\"downloadModal\" role=\"dialog\">" +
                "<div class=\"modal-dialog modal-dialog-centered\">" +
                "<div class=\"modal-content\">" +
                "<div class=\"modal-header\">" +
                "<h2 class=\"modal-title\">" + Drupal.t("Please specify the download format") + "</h2>" +
                "</div>" +
                "<div class=\"modal-body modals--border-bottom modals__body-checkboxes\">" +
                "<p>" + Drupal.t("Downloaded datas are limited to 10 000. Please, fill filters if your needed datas are not displayed.") + "</p>" +
                "<fieldset class=\"checkbox-group\">" +
                "<h3 class=\"h6 border-bottom border-ui-grey-6 pb-3 mb-3\">" + Drupal.t("Choose your exportation type") + "</h3>" +
                "<div class=\"custom-control custom-radio\">" +
                "<input class=\"custom-control-input\" id=\"download_xls\" type=\"radio\" name=\"download_format\" checked=\"checked\" value=\"excel\"/>" +
                " <label class=\"custom-control-label\" for=\"download_xls\">" + Drupal.t("MS Excel (.xlsx)") + "</label><br>" +
                "</div>" +
                "<div class=\"custom-control custom-radio\">" +
                "<input class=\"custom-control-input\" id=\"download_csv\" type=\"radio\" name=\"download_format\" value=\"csv\"/>" +
                " <label class=\"custom-control-label\" for=\"download_csv\">" + Drupal.t("Comma/dot separator (.csv)") + "</label><br>" +
                "</div>" +
                "<div class=\"custom-control custom-radio\">" +
                "<input class=\"custom-control-input\" id=\"download_txt\" type=\"radio\" name=\"download_format\" value=\"txt\"/>" +
                " <label class=\"custom-control-label\" for=\"download_txt\">" + Drupal.t("Comma/dot separator (.txt)") + "</label><br>" +
                "</div>" +
                "</fieldset>" +
                // "<div class=\"form-inline checkbox-group\">" +
                // "<span class=\"custom-control custom-radio\">" +
                // "<input class=\"custom-control-input\" id=\"layout_ver\" type=\"radio\" name=\"layout\" checked=\"checked\" value=\"ver\"/>" +
                // " <label class=\"custom-control-label\" for=\"layout_ver\">" + Drupal.t("Vertical layout") + "</label>" +
                // "</span>" +
                // "<span class=\"custom-control custom-radio\">" +
                // "<input class=\"custom-control-input\" id=\"layout_hor\" type=\"radio\" name=\"layout\" value=\"hor\"/>" +
                // " <label class=\"custom-control-label\" for=\"layout_hor\">" + Drupal.t("Horizontal layout") + "</label>" +
                // "</span>" +
                // "</div>" +
                "<fieldset class=\"checkbox-group\">" +
                "<h3 class=\"h6 border-bottom border-ui-grey-6 pb-3 mb-3\">" + Drupal.t("Decimal separator") + "</h3>" +
                "<div class=\"form-inline\">" +
                "<span class=\"custom-control custom-radio\">" +
                "<input class=\"custom-control-input\" id=\"deci_dot\" type=\"radio\" name=\"decimal\" checked=\"checked\" value=\".\"/>" +
                " <label class=\"custom-control-label\" for=\"deci_dot\">\" . \"</label>" +
                "</span>" +
                "<span class=\"custom-control custom-radio ml-4\">" +
                "<input class=\"custom-control-input\" id=\"deci_comma\" type=\"radio\" name=\"decimal\" value=\",\"/>" +
                " <label class=\"custom-control-label\" for=\"deci_comma\">\" , \"</label>" +
                "</span>" +
                "</div>" +
                "</fieldset>" +
                "<fieldset class=\"checkbox-group\">" +
                "<h3 class=\"h6 border-bottom border-ui-grey-6 pb-3 mb-3\">" + Drupal.t("Date format") + "</h3>" +
                "<div class=\"form-inline\">" +
                "<span class=\"custom-control custom-radio\">" +
                "<input class=\"custom-control-input\" id=\"date_dmy\" type=\"radio\" name=\"date_format\" checked=\"checked\" value=\"d/m/Y\"/>" +
                " <label class=\"custom-control-label\" for=\"date_dmy\">" + Drupal.t("day/month/year") + "</label>" +
                "</span>" +
                "<span class=\"custom-control custom-radio ml-4\">" +
                "<input class=\"custom-control-input\" id=\"date_mdy\" type=\"radio\" name=\"date_format\" value=\"m/d/Y\"/>" +
                " <label class=\"custom-control-label\" for=\"date_mdy\">" + Drupal.t("month/day/year") + "</label>" +
                "</span>" +
                "</div>" +
                "</fieldset>" +
                "<input type=\"submit\" class=\"btn btn-lg btn-extra-border btn-primary\" value=\"" + Drupal.t("Go") + "\"/>" +
                "</div>"
              "</div>" +
                "</div>" +
                "</div>";
              $("body").append(modal);
              $("#downloadModal").modal("toggle");
            }
          }
          ],
          columns: columnsClasses,
          columnDefs: [{
            defaultContent: "",
            orderable: false,
            targets: "no-sorting"
          },
          {
            orderable: true,
            targets: (type == 'stocks') ? 1 : 0,
            'createdCell': function (td, cellData, rowData, row, col) {
              if (jQuery(cellData).attr('data-order')) {
                $(td).attr('data-order', jQuery(cellData).attr('data-order').trim());
              }
            }
          },
          ],
          oLanguage: {
            sInfo: Drupal.t('<strong>_START_-_END_</strong> of <strong>_TOTAL_</strong> items displayed'),
            sProcessing: '<div class="customLoading"><div class="icon_loading icon_loading__x1-4"> <div class="icon_loading-arrow"></div> <div class="icon_loading-arrow icon_loading-arrow__delay"> </div></div>&emsp;' + Drupal.t("Updating") + '... </div>',
            oPaginate: {
              sNext: Drupal.t('Next') + ' <svg viewBox="0 0 24 24" width="24" height="24" role="presentation" class=""><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#arrow"></use></svg>',
              sPrevious: '<svg viewBox="0 0 24 24" width="24" height="24" role="presentation" class="icons__arrow icons__arrow--prev"><use xlink:href="' + drupalSettings.custom.asset_files_path + '/spritemap.svg#arrow"></use></svg> ' + Drupal.t('Prev'),
            },
          },
          "drawCallback": function (settings) {
            $("#stocks-data-table-es").parent().toggle(settings.fnRecordsDisplay() > 0);
            if (settings.fnRecordsDisplay() > 0) {
              $("#div-stocks-data-table-es-no-data-available").hide();
            } else {
              $("#div-stocks-data-table-es-no-data-available").show();
            }
            let currentURL = new URL(window.location.href);
            let pageEle = jQuery('a.paginate_button');
            jQuery(pageEle).each(function () {
              let pageNum = parseInt(jQuery(this).text());
              if (!(Number.isNaN(pageNum))) {
                let pageurl = currentURL.pathname + "?page=" + (pageNum - 1);
                jQuery(this).attr("href", pageurl);
              }
            });
            jQuery("a.paginate_button").on("click", function (e) {
              e.preventDefault();
            });
          }
        });
        if (type == "warrt") {
          if (checkTri == 0) {
            pd_datatables.order([[2, 'asc'], [1]]).draw();
            checkTri = 1;
          }
        }
        if (drupalSettings.help_text == "") {
          jQuery("#HelpButtonPD").remove();
        }
        if (drupalSettings.datapoints != null) {
          $("#stocks-data-table-es thead th").each(function (index) {
            if ($.inArray($(this).data("datapoints"), drupalSettings.datapoints) == "-1") {
              pd_datatables.table().column(index).visible(false);
            }
          });
        }
        // Download features
        $("body").on("click", "#downloadModal input[type=\"submit\"]", function () {
          var file_export_type = $("#downloadModal input[name=\"download_format\"]:checked").val();
          var file_export_layout = $("#downloadModal input[name=\"layout\"]:checked").val();
          var file_export_decimal_separator = $("#downloadModal input[name=\"decimal\"]:checked").val();
          var file_export_date_format = $("#downloadModal input[name=\"date_format\"]:checked").val();
          var args = {}
          args = { "fe_type": file_export_type, "fe_layout": file_export_layout, "fe_decimal_separator": file_export_decimal_separator, "fe_date_format": file_export_date_format };
          var datas = {}
          datas.iDisplayLength = pd_datatables.page.info().length;
          datas.iDisplayStart = pd_datatables.page.info().start;
          datas.args = $.extend(data_filters.args, args);
          var paramsString = "";
          for (var key in datas.args) {
            if (datas.args.hasOwnProperty(key)) {
              paramsString += encodeURIComponent(key) + "=" + encodeURIComponent(datas.args[key]) + "&";
            }
          }
          paramsString = paramsString.slice(0, -1);
          window.open(drupalSettings.jsongateway_download + "&" + paramsString);
        });
        // Create alphabet search
        var alphabet = $("<div class=\"nav nav-tabs nav-tabs-alphabet awl_pd_datas__filter__alphabet\" id=\"nav-tab-alphabet\"></div>");
        for (var i = 0; i < 26; i++) {
          var letter = String.fromCharCode(65 + i);
          $("<a href=\"#\" class=\"nav-item nav-link\" id=\"nav-tab-alphabet-" + i + "\"></a>").data("letter", letter).html(letter).appendTo(alphabet);
        }
        $("<a href=\"javascript:;\" class=\"clear nav-item nav-link\" data-others id=\"nav-tab-alphabet-" + i + "\"></span>").data("letter", "*").html(Drupal.t("Others")).appendTo(alphabet);
        $("<a href=\"javascript:;\" class=\"clear active nav-item nav-link\" data-all id=\"nav-tab-alphabet-" + i + "\"></span>").data("letter", "").html(Drupal.t("All")).appendTo(alphabet);
        alphabet.insertBefore(pd_datatables.table().container());
        alphabet.on("click", "a", function () {
          alphabetSearchTriggered = true;
          alphabet.find(".active").removeClass("active");
          $(this).addClass("active");
          var datas = $.extend(true, data_filters.args, { initialLetter: $(this).data("letter") });
          Drupal.behaviors.refresh.datas(datas);
        });
        if (drupalSettings.display_filters != "none") {
          var show_filters = $("<button type=\"button\" class=\"btn btn-lg btn-extra-border btn-primary btn-with-icon mt-4 mb-4\" data-toggle=\"modal\" data-target=\"#pageFilters-es\">" + Drupal.t("Show filters") + "<svg viewBox=\"0 0 24 24\" width=\"24\" height=\"24\"><use xlink:href=\"" + drupalSettings.custom.asset_files_path + "/spritemap.svg#settings\"></use></svg></button>");
          show_filters.insertBefore(pd_datatables.table().container());
        }
        var pd_datatables_interval, pd_datatables_timeout, pd_datatables_last_update, refreshDelay;
        awl_pd_datas_refresh();
        jQuery("#content > section div.block.block-awl-product-directory-es.block-awl-pd-datas-es-block ").append('<div class="customLoading"><div class="icon_loading icon_loading__x1-4"> <div class="icon_loading-arrow"></div> <div class="icon_loading-arrow icon_loading-arrow__delay"> </div></div>&emsp;' + Drupal.t("Updating") + '... </div>');
        function awl_pd_datas_refresh() {
          pd_datatables_interval = setInterval(function () {
            pd_datatables.ajax.reload(null, false);
          }, drupalSettings.globalRefresh);
          pd_datatables_last_update = Date.now();
        }
        window.onblur = function () {
          clearInterval(pd_datatables_interval);
          clearTimeout(pd_datatables_timeout);
        };
        window.onfocus = function () {
          var refreshDelay = 0;
          if (pd_datatables_last_update) {
            refreshDelay = (Date.now() - pd_datatables_last_update > drupalSettings.globalRefresh) ? 0 : (drupalSettings.globalRefresh - (Date.now() - pd_datatables_last_update));
          }
          pd_datatables_timeout = setTimeout(awl_pd_datas_refresh, refreshDelay);
        };
        $(document).ajaxComplete(function () {
          $('[data-toggle=tooltip]').tooltip();
          if (_isMobile()) {
            // Pagination
            // Hide all paginations and show -1 and +1 from current only
            jQuery("#stocks-data-table-es_paginate .ellipsis").remove();
            jQuery("#stocks-data-table-es_paginate > span a:not(.current)").hide();
            var current_pagination_index = jQuery("#stocks-data-table-es_paginate > span a.current").index();
            if (current_pagination_index != 0) {
              jQuery("#stocks-data-table-es_paginate > span a").eq(current_pagination_index - 1).show();
            }
            if (current_pagination_index < jQuery("#stocks-data-table-es_paginate > span a").length) {
              jQuery("#stocks-data-table-es_paginate > span a").eq(current_pagination_index + 1).show();
            }
            jQuery(".paginate_button.next").addClass("pr-0");
            jQuery(".paginate_button.previous").addClass("pl-0");
          }
          if (jQuery('div#div-stocks-data-table-es #stocks-data-table-es_wrapper').css('display') == 'none') {
            var has_data_in_filters = awl_pd_check_filter_has_data(data_filters);
            jQuery('div#div-stocks-data-table-es-no-data-available').html(
              (awl_pd_has_filter_trigger_click) ?
                _sZeroRecords :
                Drupal.t('Your search yielded no results, consider changing filters')
            );
            jQuery('div#div-stocks-data-table-es-no-data-available').show();
          } else {
            //Remove "no data available"
            // jQuery('div#div-stocks-data-table-es-no-data-available').hide();
            jQuery('table#stocks-data-table-es').css('width', '');
          }
          //show pagination if more than 100
          if (!pd_datatables || pd_datatables.settings()[0].fnRecordsDisplay() <= pd_datatables.settings()[0]._iDisplayLength) {
            jQuery("#stocks-data-table-es_paginate").css("display", "none");
            jQuery("#stocks-data-table-es").css("margin-bottom", "2%");
          } else {
            jQuery("#stocks-data-table-es_paginate").css("display", "block");
            jQuery("#stocks-data-table-es").css("margin-bottom", "0%");
          }
        });
        $(".awl_pd_datas_filters__activate").click(function () {
          $(".block-awl-pd-filters-block").toggleClass("activate");
        });
        jQuery('[id*=edit-awl-pd-filters-submit]').click(function () {
          awl_pd_has_filter_trigger_click = true;
        });
        jQuery('a[id*= nav-tab-alphabet]').click(function () {
          awl_pd_has_filter_trigger_click = false;
        });
      });
    }
  };
  Drupal.behaviors.refresh = {};
  Drupal.behaviors.refresh.datas = function (datas) {
    data_filters = Drupal.behaviors.refresh.serializeObject(datas);
    var datas = '';
    jQuery.each(data_filters.args, function (index, value) {
      if (value != "") {
        datas += index + ",";
      }
    });
    let hasFiltersChanged = datas != "";
    if (hasFiltersChanged || alphabetSearchTriggered || filterSearchTriggeredAtLeastOnce) {
      if (hasFiltersChanged) {
        filterSearchTriggeredAtLeastOnce = true;
        dataLayer.push({
          'event': 'generic',
          'e_category': 'research filters',
          'e_action': datas.replace(/,$/g, ''),
          'e_label': window.location.href
        });
      }
      if (pd_datatables != undefined) pd_datatables.ajax.reload();
    }
  };
  Drupal.behaviors.refresh.serializeObject = function (filters) {
    //old
    // var optional_parameters = ["bondCouponType", "bondIssuerName", "bondIssuerRegion", "bondIssuerType", "bondMaturity", "bondTradingType", "callPut", "capitalization", "classcification", "country", "couponType", "index", "indType", "industry", "initialLetter", "issueType", "issuerName", "localSegment", "maturity", "market", "naeCountry", "nameIsinSym", "productName", "productSegment", "region", "risk", "sector", "sectorLevel", "strategy", "strike", "subSector", "superSector", "tradingLocation", "tradingType", "underlying", "warIndustry", "warIssuer"];
    // new
    var optional_parameters = ["bondCouponType", "bondIssuerName", "bondIssuerRegion", "bondIssuerType", "bondMaturity",
      "bondTradingType", "callPut", "capitalization", "classcification", "couponType", "indType",
      "industry", "issueType", "issuerName", "issuerGroup", "localSegment", "maturity", "market", "naeCountry",
      "nameIsinSym", "productName", "productSegment", "productType", "region", "risk", "sector", "sectorLevel", "strategy", "strike",
      "subSector", "superSector", "tradingLocation", "tradingType", "warIndustry", "warIssuer", "professionalOnly", "closingTime",
      "openingTime", "underlyingType", "underlyingGroupName", "underlyingInstrument", "timeToExpiry", "eusipaName",
      "countryOfDistrib", "period", "returnRange", "groupName", "companyLongName", "underlyingCountryOfOrigin", "segment", "etfClasscification", "etfIssuerName",
      "esgClassification", "currency", "benchmarkArea", "benchmarkStyle", "pea"];
    var args = {};
    for (var i = 0; i < optional_parameters.length; i++) {
      $.each(filters, function (key, value) {
        if (value != "") {
          if ((key == "superSector" || key == "subSector") && (optional_parameters[i] == "sector")) {
            return true;
          } else {
            //878 add tradedToday filters
            if (key == "tradedToday") {
              args["tradedToday"] = "true";
            } else {
              if (key.match(new RegExp(optional_parameters[i], 'g')) != null) {
                if ((args[optional_parameters[i]]) == null) { args[optional_parameters[i]] = ""; }
                if (args[optional_parameters[i]] != "") { args[optional_parameters[i]] += ","; }
                args[optional_parameters[i]] += value;
              }
            }
          }
        }
      })
    }
    //FPLEXTOSLO-613
    if (args["region"] != undefined) {
      countCountry = (args["region"]).split(",").length;
      if (countCountry > 1) {
        args["country"] = args["region"].replace(/^[^,]+, */, '');
      } else {
        args["country"] = "0";
      }
      args["region"] = args["region"][0];
    }
    args[initialLetter] = (typeof $(".awl_pd_datas__filter__alphabet a.active").attr("data-all") !== "undefined") ? "" : (typeof $(".awl_pd_datas__filter__alphabet a.active").attr("data-others") !== "undefined") ? "*" : $(".awl_pd_datas__filter__alphabet a.active").html();
    return { args: args };
  }
})(jQuery, Drupal, drupalSettings);
function _isMobile() {
  if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || jQuery(window).width() < 426) return true;
  return false;
}
function awl_pd_check_filter_has_data(data) {
  var hasdata = false;
  for (key in data) {
    if (data[key] !== null && typeof (data[key]) === 'object') {
      hasdata = awl_pd_check_filter_has_data(data[key])
    } else {
      if (data[key] !== null && data[key] !== "" && data[key] !== undefined) {
        hasdata = true;
      }
    }
  }
  return hasdata;
}
window.onresize = function () {
  if (window.innerWidth <= 1270) {
  }
}

/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/modules/custom/awl_product_directory_es/js/awl-pd-es.js. */