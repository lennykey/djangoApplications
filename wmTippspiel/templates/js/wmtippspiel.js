$(document).ready(function() {
  $("#gruppen").hide(); 
                                      
  $("#toggle").toggle(
      function () {
        $("#gruppen").show(); 

      },
      function () {
         $("#gruppen").hide(); 
      }
    );

/*   $("#spielregelncontent").hide(); */ 
     $("#spielregelnheaddown").hide();
	 
	$('#spielregelnheadup').click(function() {
          $("#spielregelncontent").slideUp(); 
		  $("#spielregelnheaddown").show();
		  $("#spielregelnheadup").hide();

    });
	
	$('#spielregelnheaddown').click(function() {
          $("#spielregelncontent").slideDown(); 
		   $("#spielregelnheaddown").hide();
		   $("#spielregelnheadup").show();

    });
	
	$('#tippsofbegegnung').hide();
	$('.begegnungid').hide();
	
	
	
	$('#usertippsclose').click(
	   function(){
	        $('#tippsofbegegnung').slideUp();
	   }
	);
	
	$('#tippsofbegegnung').click(
	   function(){
	        $('#tippsofbegegnung').slideUp();
	   }
	);
	
	$('.vergleichzeile').click(
	   function(){
	   	   var $id = $(this).children('.begegnungid').text();
		   var $link = '/wmtippspiel/tippspiel/tippsofbegegnung/' + $id;
		   
	       $('#tippsofbegegnung').load($link);
		   
		   $('#tippsofbegegnung').slideDown(); 
		   
	   }
	);
	
	
	$('#tippformframe').hide();
    $('.tippen').click(
       function(){
	       var $id = $(this).children().attr('name');
		   /*
		   $id= $id.split('/');
		   $id= $id[5];
		   alert($id)
           */
		  
           var $link = '/wmtippspiel/tippspiel/tippen/tipp-form/' + $id;
		  
           $('#tippformframe').show();
		   $('#tippform').slideDown();
           $('#tippform').load($link);
           
       }
    );
	
	$('.tippaendern').click(
       function(){
           var $id = $(this).attr('name');
           /*
           $id= $id.split('/');
           $id= $id[5];
           alert($id)
           */
          
           var $link = '/wmtippspiel/tippspiel/tippen/tipp-form/' + $id;
		   $('#tippformframe').show();
		   $('#tippform').slideDown();
           $('#tippform').load($link);
           
       }
    );
	

	
	$('#schliessen').click(
       function(){
           $('#tippformframe').hide();
       }
    );
    
    
/*    
    $('#spielregelnhead').mouseover(function() {
         $('#spielregelncontent').show()
    });
    
    $('#spielregelnhead').mouseout(function() {
         $('#spielregelncontent').hide()
    });
*/
    
});