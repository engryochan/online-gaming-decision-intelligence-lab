/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/modules/custom/awl_mobile_search_menu/js/awl-mobile-search-menu.js. */
jQuery(document).ready(function() {

	if (jQuery('#mobile-search-menu').length) {
		jQuery('#mobile-search-menu').mmenu();

		jQuery('#awl_mobile_search_menu_link').click(function(){
			jQuery('.block-awlmobilesearchmenu form').show();
		});

		jQuery('#mobile-search-menu .header__form').each(function() {
			jQuery(this).addClass('mr-4 ml-4');
		});

		jQuery('#mobile-search-menu .header__form:first').addClass('mb-6');

		jQuery('#mobile-search-menu .form-submit').addClass('text-white');
	}
});

/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/modules/custom/awl_mobile_search_menu/js/awl-mobile-search-menu.js. */