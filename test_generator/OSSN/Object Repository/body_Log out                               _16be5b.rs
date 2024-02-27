<?xml version="1.0" encoding="UTF-8"?>
<WebElementEntity>
   <description></description>
   <name>body_Log out                               _16be5b</name>
   <tag></tag>
   <elementGuidId>c408590e-8e4c-4f5c-9715-9c7a64010829</elementGuidId>
   <selectorCollection>
      <entry>
         <key>XPATH</key>
         <value>//body</value>
      </entry>
      <entry>
         <key>CSS</key>
         <value>body</value>
      </entry>
   </selectorCollection>
   <selectorMethod>XPATH</selectorMethod>
   <useRalativeImagePath>true</useRalativeImagePath>
   <webElementProperties>
      <isSelected>false</isSelected>
      <matchCondition>equals</matchCondition>
      <name>tag</name>
      <type>Main</type>
      <value>body</value>
   </webElementProperties>
   <webElementProperties>
      <isSelected>true</isSelected>
      <matchCondition>equals</matchCondition>
      <name>text</name>
      <type>Main</type>
      <value>
	
    		
            	
            
    

	
	
	
    
	
    	
        
        	
			
            			            			
                         
            		
                            	
						
                        
                        	 
    						
             					 Log out
           					 
      		    		
                        
           		
                        	        
        
        
    
    		
    	  
    
   			 
     			 
   			 
        		
            		
            			DashboardHelpPremium VersionView Site
									  Configure
									  OssnWallNotificationsAds ManagerSite PagesSmiliesGiphy            		
            		
						 ComponentsComponentsInstallerThemesThemesInstallerGoBlueSite SettingsBasicCacheUser ManagerList UsersAdd UserUnvalidated Users           		 	                    
        		
    		

    	
    	
    	
        	
            	 
	
	   
	  	 
       			
    				
You are now logged in!
                                    		
	   	
	
    
    
    
    	
			Dashboard
    	 	
	
    
    	
        	
        		Users
            	
            			
                        2021
           	 	
            
        

    
    
    
            
        	
        		Users (4)
            	
               			
                        MaleFemale         			
           	 	
            
        

        
        	
        		Unvalidated Users
            	
                        
                        	0                                             
           	 	
            
        
        
        
        
        	
        		Users Online (1)
            	
                        	
                            Male     
           	 	
            
        
                
    
	
    
 
         
        	
        		Components
            	
                        
                        	23                                         
           	 	
            
           
 
         
        	
        		Themes
            	
                        
                            1                                       
           	 	
            
           
 
          
        	
        		My OSSN Files Version
            	
                        
                            6.1                                             
           	 	
            
           
            
    
    
    
          
        	
        		Available Updates
            	
                        ---                       
           	 	
            
               
    
          
        	
        		My OSSN Version
            	
                        
                            6.1                                             
           	 	
            
             
          
        	
        		Cache
            	
                        
                           	Flush Cache
                                            
           	 	
            
           
                    
    






		/**
		 * Get data for last two years
		 */
		var lineChartData = {
			labels : [&quot;January&quot;,&quot;February&quot;,&quot;March&quot;,&quot;April&quot;,&quot;May&quot;,&quot;June&quot;,&quot;July&quot;,&quot;August&quot;,&quot;September&quot;,&quot;October&quot;,&quot;November&quot;,&quot;December&quot;],
			datasets : [
									{
					label: &quot;2021&quot;,
					fillColor : &quot;rgba(151,187,205,0.2)&quot;,
					strokeColor : &quot;rgba(151,187,205,1)&quot;,
					pointColor : &quot;rgba(151,187,205,1)&quot;,
					pointStrokeColor : &quot;#fff&quot;,
					pointHighlightFill : &quot;#fff&quot;,
					pointHighlightStroke : &quot;rgba(151,187,205,1)&quot;,					
					data : [0,0,0,0,0,0,0,0,0,3,1,0]				}	
											]
		}
		/**
		 * Generate a graph on page load
		 */		
		$(document).ready(function(){
			var ctx = document.getElementById(&quot;users-count-graph&quot;).getContext(&quot;2d&quot;);
			var myLine = new Chart(ctx).Line(lineChartData, {
				responsive: true,
				maintainAspectRatio: false,
			});
			//don't you want lagends ? $arsalanshah
			//comment line below if you want to hide legends
			chart_js_legend(document.getElementById(&quot;usercount-lineLegend&quot;),lineChartData);

		});
	
		/**
		 * Get data for last two years
		 * Translation for gender in dashboard users &amp; users online #511		 
		 */
		var gdata = [
{
value: 1,
color: '#01ADEF',
highlight: '#01ADEF',
label: 'Male'
},
{
value: 3,
color: '#ED008C',
highlight: '#ED008C',
label: 'Female'
},
			];
			$(window).on('load', function(){
				var chartjs = $('#users-classified-graph')[0].getContext(&quot;2d&quot;);
				this.myPie = new Chart(chartjs).Pie(gdata);
			    //don't you want lagends ? $arsalanshah
				//comment line below if you want to hide legends
				chart_js_legend($('#userclassified-lineLegend')[0],gdata);				
			});
	

		/**
		 * Get data for last two years
		 * Translation for gender in dashboard users &amp; users online #511
		 */
		var OnlineUsersPieData = [
{
value: 1,
color: '#01ADEF',
highlight: '#01ADEF',
label: 'Male'
},
			];
			$(window).on('load', function(){
				var online_users_graph = $('#onlineusers-classified-graph')[0].getContext(&quot;2d&quot;);
				this.OnlinemyPie = new Chart(online_users_graph).Pie(OnlineUsersPieData);
			    //don't you want lagends ? $arsalanshah
				//comment line below if you want to hide legends
				chart_js_legend($('#onlineuserclassified-lineLegend')[0], OnlineUsersPieData);				
			});			
	
    	
	
                
        
        
        
        
      	  	
        		
 				© COPYRIGHT 2021 OSSN            			
           	 	
                
                	 POWERED OPEN SOURCE SOCIAL NETWORK                
        	
        
        
     


/html[1]/body[1]/div[@class=&quot;topbar-menu&quot;]/nav[@class=&quot;navbar navbar-expand-lg navbar-default navbar-admin-second&quot;]/div[@class=&quot;container&quot;]/button[@class=&quot;navbar-toggler&quot;]/i[@class=&quot;fa fa-bars&quot;]</value>
   </webElementProperties>
   <webElementProperties>
      <isSelected>false</isSelected>
      <matchCondition>equals</matchCondition>
      <name>xpath</name>
      <type>Main</type>
      <value>/html[1]/body[1]</value>
   </webElementProperties>
   <webElementXpaths>
      <isSelected>true</isSelected>
      <matchCondition>equals</matchCondition>
      <name>xpath:position</name>
      <type>Main</type>
      <value>//body</value>
   </webElementXpaths>
</WebElementEntity>
