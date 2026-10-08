/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/themes/custom/euronext_live/js/internal-menu-scroll.js. */
(function (Drupal) {
  Drupal.behaviors.scrollableInternalMenu = {
    attach: function (context) {
      'use strict'

      const internalMenu = once('internal-menu-el', document.getElementsByClassName('menu--inpage-navigation'))[0];
      if (!internalMenu) {
        return;
      }
      const menuItemsScroll = internalMenu.querySelector('.internal-menu__scroll');
      const menuItemsWrap = menuItemsScroll.querySelector('.internal-menu__wrap');
      const prevBtn = internalMenu.querySelector('.internal-menu__scroll-left');
      const nextBtn = internalMenu.querySelector('.internal-menu__scroll-right');
      const menuItems = menuItemsWrap.querySelectorAll('.nav-item');


      // Helper function
      function debounce(func, delay) {
        let timeoutId;
        return (...args) => {
          const context = this;
          clearTimeout(timeoutId);
          timeoutId = setTimeout(() => {
            func.apply(context, args);
          }, delay);
        };
      }

      let currentIndex = 0; // Tracks the index of the first visible item
      // Ensure there are items before trying to get computed style
      let itemMarginRight = menuItems.length > 0 ? parseFloat(getComputedStyle(menuItems[0]).marginRight) : 0;
      // Calculate the maximum scrollable width
      let maxScrollLeft = menuItemsWrap.scrollWidth - menuItemsScroll.clientWidth;

      /**
       * Updates the state of the navigation buttons (enabled/disabled/hidden).
       * Buttons are hidden if no scrolling is needed, otherwise enabled/disabled based on position.
       */
      const updateButtonStates = () => {
        const tolerance = 5; // Pixels for floating point inaccuracies

        // Calculate the total width of all menu items (including margins)
        let totalContentWidth = 0;
        menuItems.forEach(item => {
          totalContentWidth += item.offsetWidth + itemMarginRight;
        });
        // Subtract the last item's margin as it doesn't add to the container's total scrollable width
        // Because we took the margin of the first item.
        if (menuItems.length > 0) {
          totalContentWidth -= itemMarginRight;
        }

        // If total content width is less than or equal to the wrapper's visible width, hide both buttons
        if (totalContentWidth <= menuItemsScroll.clientWidth + tolerance) {
          prevBtn.classList.add('is-hidden');
          nextBtn.classList.add('is-hidden');
        } else {
          // Otherwise, ensure buttons are visible
          prevBtn.classList.remove('is-hidden');
          nextBtn.classList.remove('is-hidden');

          // Disable prevBtn if at the beginning of the scrollable area
          prevBtn.disabled = menuItemsScroll.scrollLeft <= tolerance;

          // Disable nextBtn if at the end of the scrollable area
          // When scrollLeft + clientWidth is approximately equal to scrollWidth, we are at the end.
          nextBtn.disabled = (menuItemsScroll.scrollLeft + menuItemsScroll.clientWidth >= menuItemsScroll.scrollWidth - tolerance);
        }
      };

      /**
       * Scrolls the menu to the target item based on the direction.
       * @param {string} direction - 'left' or 'right'.
       */
      const scrollMenu = (direction) => {
        let targetScrollLeft = 0;
        let newIndex = currentIndex;

        if (direction === 'right') {
          if (currentIndex < menuItems.length - 1) {
            newIndex++;
          }
        } else if (direction === 'left') {
          if (currentIndex > 0) {
            newIndex--;
          }
        }

        // Calculate the horizontal scroll position needed to bring the new index into view
        for (let i = 0; i < newIndex; i++) {
          // Add the width of each menu item and its right margin
          targetScrollLeft += menuItems[i].offsetWidth + itemMarginRight;
        }

        // Recalculate the maximum scrollable width
        maxScrollLeft = menuItemsWrap.scrollWidth - menuItemsScroll.clientWidth;
        // Set the scroll position, but do not exceed the maximum allowed
        menuItemsScroll.scrollLeft = Math.min(targetScrollLeft, maxScrollLeft);

        currentIndex = newIndex; // Update the current index
        updateButtonStates(); // Update button states after scrolling
      };

      // Event listeners for navigation buttons
      prevBtn.addEventListener('click', () => scrollMenu('left'));
      nextBtn.addEventListener('click', () => scrollMenu('right'));

      // Listen for scroll events on the wrapper to update button states if user scrolls manually
      menuItemsScroll.addEventListener('scroll', debounce(() => {
        updateButtonStates();
      }, 100));

      // Initial update of button states when the page loads
      updateButtonStates();

      // Recalculate button states on window resize to handle responsiveness
      window.addEventListener('resize', debounce(() => {
        currentIndex = 0; // Reset index
        menuItemsScroll.scrollLeft = 0; // Reset scroll position
        itemMarginRight = menuItems.length > 0 ? parseFloat(getComputedStyle(menuItems[0]).marginRight) : 0; // Recalculate margin
        maxScrollLeft = menuItemsWrap.scrollWidth - menuItemsScroll.clientWidth; // Recalculate max scroll width
        updateButtonStates();
      }, 100));
    }

  }
})(Drupal);

/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/themes/custom/euronext_live/js/internal-menu-scroll.js. */