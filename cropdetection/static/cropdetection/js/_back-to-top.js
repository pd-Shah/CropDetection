jQuery(document).ready(function() {
	var offset = 220;
	var duration = 500;
	
		jQuery(window).scroll(function() {
		if (jQuery(this).scrollTop() > offset) {
			jQuery('.cd-top').fadeIn(duration);
			} else {
				jQuery('.cd-top').fadeOut(duration);
				}
			});
				
		jQuery('.cd-top').click(function(event) {
			event.preventDefault();
			jQuery('html, body').animate({scrollTop: 0}, duration);
			return false;
		})
	});