/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/themes/custom/euronext_base/js/responsive_menu.js. */
(function ($) {

  'use strict';

  /**
   * Provides the off-canvas menu customisation.
   */
  Drupal.behaviors.responsive_menu_custom = {
    attach: function (context) {

      const mmenuId = '#off-canvas';
      const offCanvas = document.querySelector(mmenuId)

      function getActiveElement(currentUrl, selectorElement) {
        let splitCurrentUrl = currentUrl.split('/');

        // Return the active element if the item is already selected.
        let activeElement = selectorElement.querySelector('li.mm-listitem_selected > a:first-child');
        if (activeElement && typeof activeElement != 'undefined' && activeElement.nextElementSibling) {
          return activeElement;
        }

        // Find the related list element based on url to get the active hierarchy.
        for (let i = splitCurrentUrl.length; i > 0; i--) {
          let lookoutUrl = splitCurrentUrl.slice(0, i).join('/');
          activeElement = selectorElement.querySelector('a[href="' + lookoutUrl + '"], a[href="' + lookoutUrl + '"], a[href="' + lookoutUrl + '/"]');
          if (activeElement && activeElement.nextElementSibling) {
            return activeElement;
          }
        }

        // if url has no langcode, menu links will have, so retry by search ending href
        // Find the related list element based on url to get the active hierarchy.
        for (let i = splitCurrentUrl.length; i > 0; i--) {
          let lookoutUrl = splitCurrentUrl.slice(0, i).join('/');
          activeElement = selectorElement.querySelector('a[href$="' + lookoutUrl + '"], a[href$="' + lookoutUrl + '/"]');
          if (activeElement && activeElement.nextElementSibling) {
            return activeElement;
          }
        }
      }

      // The instatiation of the mmenu must only happen once.
      if (offCanvas && offCanvas.hasOwnProperty('mmApi') && typeof (Mmenu) !== 'undefined') {

        const mmenuApi = offCanvas.mmApi;
        var firstOccurance = true;

        mmenuApi.bind('open:before', function() {
          // Open the parent item's panel if parent item is link and active.
          if (firstOccurance) {
            const currentHref = window.location.href;
            const getCurrentUrl = function() {
              var currentHref = window.location.href;
              currentHref = currentHref.split("?")[0].split("#")[0];
              var url = new URL(currentHref);
              return currentHref.replace(url.origin, '');
            }
            const currentUrl = getCurrentUrl(currentHref);
            const activeElement = getActiveElement(currentUrl, this.node.menu);
            if (activeElement) {
              activeElement.nextElementSibling.click();
            }
            firstOccurance = false;
          }

          var currentElement = $(this.node.menu).find('.mm-panel_opened')[0];
          if (typeof currentElement !== 'undefined' && typeof currentElement.mmParent !== 'undefined') {

            var text = $(currentElement).find('.mm-navbar_sticky .mm-navbar__title')[0].innerText;
            var href = '#';
            if (typeof currentElement.mmParent !== 'undefined') {
              href = $(currentElement.mmParent).find('a:contains("' + text + '")').attr('href')
            }
            var titleElement = document.createElement('li');
            titleElement.classList.add('mm-listitem');
            titleElement.innerHTML = href.startsWith('#')
              ? '<strong class="mm-listitem__text">' + text + '</strong>'
              : '<a href="'+ href +' "class="mm-listitem__text"><strong>' + text + '</strong></a>';

            if ($(currentElement).find('ul.mm-listview')[0].firstElementChild.innerHTML !== titleElement.innerHTML) {
              $(currentElement).find('ul.mm-listview')[0].prepend(titleElement);
            }
          }
        });

        mmenuApi.bind("openPanel:before", function (panel) {
          if (typeof panel.mmParent !== 'undefined') {
            var text = panel.mmParent.children[0].firstChild.data;

            var srcElement = $(panel).find('.mm-navbar_sticky').find('.mm-navbar__title').attr('href')
            var href = srcElement ? $(srcElement).find('a:contains("' + text + '")').attr('href') : '#';
            var titleElement = document.createElement('li');
            titleElement.classList.add('mm-listitem');

            titleElement.innerHTML = href.startsWith('#')
              ? '<strong class="mm-listitem__text">' + text + '</strong>'
              : '<a href="'+ href +' "class="mm-listitem__text"><strong>' + text + '</strong></a>';

            if (panel.querySelector('ul.mm-listview').firstElementChild.innerHTML !== titleElement.innerHTML) {
              panel.querySelector('ul.mm-listview').prepend(titleElement);
            }
          }
        });

      }
    }
  };
})(jQuery);


/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/themes/custom/euronext_base/js/responsive_menu.js. */