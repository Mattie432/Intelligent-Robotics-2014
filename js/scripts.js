$(function(){

	var main_img = $('#image_main');
	$('#image_switcher').find('img').each(function(){
		$(this).on('click', function(){
			var new_image = $(this).attr("data-full");
			
			if(new_image != "FADE_OVER"){
				main_img.attr('src', new_image);
				$(this).parent().parent().find('.active_tab').removeClass('active_tab');
				$(this).parent().addClass('active_tab');
			} else {
				return;
			}

		});
	});

	$('#more_hardware').click(function(){$('#hardware_continue').toggle();});
	$('#more_software').click(function(){$('#software_continue').toggle();});
	$('#more_local').click(function(){$('#local_continue').toggle();});
	$('#more_people').click(function(){$('#people_continue').toggle();});
	$('#more_explore').click(function(){$('#explore_continue').toggle();});
	$('#more_control').click(function(){$('.control_continue').toggle();});


});