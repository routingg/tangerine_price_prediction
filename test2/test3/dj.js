$(".progress-bar").on("click", function(e) {
  var offset = $(this).offset(),
      position = Math.floor((e.pageX - offset.left)/$(this).width()*100) + 1;
  $(this).find('.progress-bar__bar').css('transform','translateX('+position+'%)'); 
  $(this).find('.progress-bar__bar').css('-webkit-transform','translateX('+position+'%)');
});

// Send bar to random point
$(document).ready(function(){
  $('.progress-bar__bar').each(function(){
		$(this).css('transform','translateX('+Math.random()*100+'%)'); 
  	$(this).css('-webkit-transform','translateX('+Math.random()*100+'%)');
	});
});
