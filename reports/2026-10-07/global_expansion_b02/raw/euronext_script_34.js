/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/assets/asset_injector/js/ah_display_message_on_youtube_videos_when_no_consent-825de5f9c5e35b09bac7a36e03bfd02a.js. */
(function($) {

	var z = 0;
	
	$("iframe").each(function(){
		if($(this).attr("src")){
			if($(this).attr("src").indexOf("youtube.com") > -1 || $(this).attr("src").indexOf("//youtu.be/") > -1 || $(this).attr("src").indexOf("wistia.com") > -1){
				z++;
			}
		}
		else if($(this).attr("data-src")){
			if($(this).attr("data-src").indexOf("youtube.com") > -1 || $(this).attr("data-src").indexOf("//youtu.be/") > -1){
				z++;
			}
		}
	});
	
	if(z > 0){
		const intervalIdIframes = setInterval(updateIframes, 1000);
		localStorage.setItem('intervalIdIframes', intervalIdIframes);
		
		if($(".embed-responsive-16by9").html() != undefined){		
			$(".embed-responsive-16by9").each(function(){
					var gClass = makeid(10);
					var width = $(this).width();
					var height = width * 0.5625;
					$(this).addClass(gClass);
					
					$("."+gClass+" [id^=iframe-wrapper]").css("width",width);		
					$("."+gClass+" [id^=iframe-wrapper]").css("height",height);
					
			});
			
			$(window).on('resize', function(){
				$(".embed-responsive-16by9").each(function(){
						var gClass = makeid(10);
						var width = $(this).width();
						var height = width * 0.5625;
						$(this).addClass(gClass);
						
						$("."+gClass+" [id^=iframe-wrapper]").css("width",width);		
						$("."+gClass+" [id^=iframe-wrapper]").css("height",height);
				});
			});
		}
		
		if($(".video-embed-field-provider-youtube").html() != undefined){
			getWidth();
			
			$(window).on('resize', function(){
				getWidth();
			});
			
			if(getCookie("OptanonConsent").indexOf(",C0004:0,") != -1){	
				$(".accordion__header h5 button").on('click', function(){
					
					setTimeout(function (){						  
						getWidth();	
					}, 100);
				});
			}
		}
	}
	
	if($(".youtube-playlist__player").html() != undefined){
		const intervalId = setInterval(updatePlaylistIframe, 1000);
		localStorage.setItem('intervalId', intervalId);
		
		var width = $(".youtube-playlist__player").width();
		// var height = $(".youtube-playlist__player").height();
			var height = width * 0.5625;
		
		$("[id^=playlist_iframe-wrapper]").css("width",width);		
		$("[id^=playlist_iframe-wrapper]").css("height",height);
		
		$(window).on('resize', function(){
			var width = $(".youtube-playlist__player").width();
			// var height = $(".youtube-playlist__player").height();
				var height = width * 0.5625;
			
			$("[id^=playlist_iframe-wrapper]").css("width",width);		
			$("[id^=playlist_iframe-wrapper]").css("height",height);
		});
	}
	
	function getWidth(){
		$(".video-embed-field-provider-youtube").each(function(){
			var gClass = makeid(10);
			var width = $(this).width();
			var height = width * 0.5625;
			$(this).addClass(gClass);
			
			$("."+gClass+" [id^=iframe-wrapper]").css("width",width);		
			$("."+gClass+" [id^=iframe-wrapper]").css("height",height);
		});
	}
	
	function updatePlaylistIframe(){
		var i = 1;
		
		if(getCookie("OptanonConsent").indexOf(",C0004:1,") != -1){	
			clearInterval(localStorage.getItem('intervalId'));
			$(".youtube-playlist__player iframe").each(function(){
				var iframe = $(this).parent().html().replace('data-src=','src=');
				iframe = iframe.replace('optanon-category-C0004','');
				$(this).parent().html(iframe);
				
				$("[id^=playlist_placeholder]").css("display","none");
			});
		}
		else{
			if($("#playlist_placeholder_1").html() != undefined){
				clearInterval(localStorage.getItem('intervalId'));
				
			}
			else{
				$(".youtube-playlist__player iframe").each(function(){
					var width = $(".youtube-playlist__player").width();
					// var height = $(".youtube-playlist__player").height();
					var height = width * 0.5625;
					
					$(this).parent().addClass("playlist_iframe_container_"+i);
					
					var src = $(this).attr("src");
					
					var iframe = $(this).parent().html().replace(' src=',' data-src=');
					
					iframe = iframe.replace('class="embed-responsive-item"','class="embed-responsive-item optanon-category-C0004"');
					
					
					var html_before = '<div id="playlist_iframe-wrapper_'+i+'"><div id="playlist_placeholder_'+i+'"><p>Playing this video will load a content from YouTube, a service of Google LLC. For information on how Google may use your data, see the <a href="https://policies.google.com/privacy" target="_blank">Google privacy policy</a>.</p><br> <div><div href="" class="btn btn-lg btn-primary" onclick="OneTrust.UpdateConsent(\'Category\',\'C0004:1\');">Accept cookies</div></div></div><script type="text/plain" class="optanon-category-C0004"> document.getElementById("playlist_placeholder_'+i+'").style.display = "none";</script>';
					var html_after = '</div><style type="text/css">* {box-sizing: border-box;margin: 0;} .embed-responsive-16by9::before {padding-top: 0%;} #playlist_iframe-wrapper_'+i+' {z-index: 100; position: relative;width: '+width+'px;height: '+height+'px;border: 1px solid gray;} #playlist_placeholder_'+i+' {z-index: 100; position: absolute;height: 100%;width: 100%;top: 0;left: 0;display: flex; flex-direction: column;justify-content: center;align-items: center;} #playlist_placeholder_'+i+' * {margin: 4px;} </style>';
					
					var new_iframe = html_before+' '+iframe+' '+html_after;
					
					$(".playlist_iframe_container_"+i).html(new_iframe);
				});
			}
		}
	}
	
	function wrap_youtube_video(iframe, classF, width, height, src, i){	
					
		if(getCookie("OptanonConsent").indexOf(",C0004:1,") != -1){}
		else{
			if(src.indexOf("wistia.com") > -1){
			
			}
			else{			
				var html_before = '<div id="iframe-wrapper_'+i+'"><div id="placeholder_'+i+'"><p>Playing this video will load a content from YouTube, a service of Google LLC. For information on how Google may use your data, see the <a href="https://policies.google.com/privacy" target="_blank">Google privacy policy</a>.</p><br> <div><div href="" class="btn btn-lg btn-primary" onclick="OneTrust.UpdateConsent(\'Category\',\'C0004:1\');">Accept cookies</div></div></div><script type="text/plain" class="optanon-category-C0004"> document.getElementById("placeholder_'+i+'").style.display = "none";</script>';
				var html_after = '</div><style type="text/css">* {box-sizing: border-box;margin: 0;} .embed-responsive-16by9::before {padding-top: 0%;} #iframe-wrapper_'+i+' {z-index: 100; position: relative;width: '+width+'px;height: '+height+'px;border: 1px solid gray;} #placeholder_'+i+' {z-index: 100; position: absolute; background-color: #ffffff; height: 100%;width: 100%;top: 0;left: 0;display: flex; flex-direction: column;justify-content: center;align-items: center;} #placeholder_'+i+' * {margin: 4px;} </style>';
			
				var new_iframe = html_before+' '+iframe+' '+html_after;
				
				if(width < 400){
					new_iframe = new_iframe+"<style>#iframe-wrapper_"+i+" p {font-size: 10px!important;</style>";
				}
				
				$("."+classF).html(new_iframe);
			}
			
			
		}
	}

	function getCookie(cname) {
	  let name = cname + "=";
	  let decodedCookie = decodeURIComponent(document.cookie);
	  let ca = decodedCookie.split(';');
	  for(let i = 0; i <ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == ' ') {
		  c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
		  return c.substring(name.length, c.length);
		}
	  }
	  return "";
	}
	
	function updateIframes(){
		if($("#iframe-wrapper_1").html() != undefined){
			clearInterval(localStorage.getItem('intervalIdIframes'));
		}
		else{
			var i = 1;
		
			$("iframe:not(.youtube-playlist__player iframe)").each(function(){
				
				if($(this).attr("src")){
					if($(this).attr("src").indexOf("youtube.com") > -1 || $(this).attr("src").indexOf("//youtu.be/") > -1 || $(this).attr("src").indexOf("wistia.com") > -1){
						$(this).parent().addClass("iframe_container_"+i);
						
						if($(this).attr("src").indexOf("//youtu.be/") > -1){
							
							var width = $(this).parent().width();
							var height = width * 0.5625;
							// var height = $(this).parent().height();
							
							var iframe = $(this).parent().html().replace(' src=',' data-src=');
							iframe = iframe.replace('class="media-oembed-content"','class="media-oembed-content optanon-category-C0004"');
							iframe = iframe+"<style>#iframe-wrapper_"+i+" {margin-top: 0%!important;</style>";
						}
						else if($(".video-embed-field-provider-youtube").html() != undefined){
							var width = $(this).parent().width();
							var height = width * 0.5625;
							// var height = $(this).parent().height();
							
							var iframe = $(this).parent().html().replace(' src=',' data-src=');
							iframe = iframe.replace('<iframe','<iframe class="optanon-category-C0004"');
							
							iframe = iframe+"<style>.video-embed-field-responsive-video::after {padding-bottom: 0%!important;}</style>";
							
						}
						else if($(".embed-responsive-16by9").html() != undefined){
							var width = $(this).parent().width();
							var height = width * 0.5625;
							// var height = $(this).parent().height();
							
							var iframe = $(this).parent().html();
							iframe = iframe+"<style>.embed-responsive-16by9::after {padding-bottom: 0%!important;}</style>";
							
						}
						else{
							var width = $(this).attr("width");
							var height = width * 0.5625;
							// var height = $(this).attr("height");
							
							var iframe = $(this).parent().html();
						}
						
						var src = $(this).attr("src");
						
						
						wrap_youtube_video(iframe, "iframe_container_"+i, width, height, src, i);
						i++
					}
				}
				else if($(this).attr("data-src")){
					if($(this).attr("data-src").indexOf("youtube.com") > -1 || $(this).attr("data-src").indexOf("//youtu.be/") > -1){
						$(this).parent().addClass("iframe_container_"+i);
						
						if($(this).attr("data-src").indexOf("//youtu.be/") > -1){
							
							var width = $(this).parent().width();
							var height = $(this).parent().height();
							
							var iframe = $(this).parent().html();
							iframe = iframe.replace('class="media-oembed-content"','class="media-oembed-content optanon-category-C0004"');
							iframe = iframe+"<style>#iframe-wrapper_"+i+" {margin-top: 0%!important;</style>";
						}
						else if($(".video-embed-field-provider-youtube").html() != undefined){
							var width = $(this).parent().width();
							var height = $(this).parent().height();
							
							var iframe = $(this).parent().html();
							iframe = iframe+"<style>.video-embed-field-responsive-video::after {padding-bottom: 0%!important;</style>";
							
						}
						else if($(".embed-responsive-16by9").html() != undefined){
							var width = $(this).parent().width();
							var height = $(this).parent().height();
							
							var iframe = $(this).parent().html();
							iframe = iframe+"<style>.embed-responsive-16by9::after {padding-bottom: 0%!important;}</style>";
							
						}
						else{
							var width = $(this).attr("width");
							var height = $(this).attr("height");
							
							var iframe = $(this).parent().html();
						}
						
						var src = $(this).attr("data-src");
						
						
						wrap_youtube_video(iframe, "iframe_container_"+i, width, height, src, i);
						i++
					}
				}
				
				
			});
		}
	}
	
	function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
	}

})(jQuery);
/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/assets/asset_injector/js/ah_display_message_on_youtube_videos_when_no_consent-825de5f9c5e35b09bac7a36e03bfd02a.js. */