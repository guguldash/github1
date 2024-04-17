var debugLevel = 2; //1,2,3,4,5.
session_info = {"ver":"0.18.7"}

function launch(pg,win){
	if (win === 'web'){
		p = window.open(pg,'_self','fullscreen=yes');
		p.focus();
	}
	
	if (win === 'mob'){
		p=window.open(pg,'ThinkarMobile','popup=yes');
		p.focus();
		p.resizeTo(400,650);
		p.moveTo(500,40);		
	}

	if (win === 'tab'){
		p = window.open(pg,'ThinkarTab','popup=yes,left=40,top=40,width=1280,height=820');
		p.focus();
	}
}

function bind_events(){
	$("[data-do]").unbind().bind('click', function(e) {
		x_do($(this).data('do'), $(this).data('form'));		
	});

	$("[data-nav]").unbind().bind('click', function(e) {
		x_nav($(this).data('nav'));		
	});

	$("[data-enter]").unbind().bind('keydown', function(e) {
		console.log($(this).data('enter'))
		if (e.key === "Enter") {
			eval($(this).data('enter'));	
			return false;
		}
	});

}

function x_nav(_route){	
	console.log(_route);
	if (x_routes[_route.split('/')[0]] === undefined){x_log('Invalid Route..',1); return;}
	history.pushState(_route, "", "");
	x_load(_route);
}

function x_load(_url){
	//A RouteKey can have an an x-api to call, x-page to render,x-event to raise and a x-div to load page to.
	routeKey = _url.split('/')[0]
	//params = _url.split('/')[1]
	params = _url.replace(_url.split('/')[0],'')

	console.log(routeKey)
	console.log(x_routes[routeKey])
	if (x_routes[routeKey].x_api !== undefined){
		var api_url = x_routes[routeKey].x_api
		if (params !== '') {api_url += params} 
		else {if (!(api_url.endsWith('/'))) {api_url += '/'}}
		
		x_log(api_url,1);

		$.ajax({
		  url: api_url,
		  headers: {"x-ses": JSON.stringify(session_info.user)},
		  dataType: 'json'
		}).done(json => x_render(routeKey, json));

		//$.getJSON(api_url).done(json => x_render(routeKey, json));
	}
	else{
		x_render(routeKey);
	}	
}

function x_render(routeKey,json){
    var purl = x_routes[routeKey].x_page;
	var div = "x-body";
	if (x_routes[routeKey].x_div !== undefined){div = x_routes[routeKey].x_div;} 
    
	var env = nunjucks.configure([''], { autoescape: false });
	console.log(session_info)
	env.addGlobal('ses', session_info);
	try {
		clear_state();
		document.getElementById(div).innerHTML = nunjucks.render(purl, json);
	} catch (e) {
		x_log(e,1);
	}
	
	if (x_routes[routeKey].x_code !== undefined){loadScript(x_routes[routeKey].x_code)}
	bind_events();
}

function x_do(_url, _formname){
	routeKey = _url.split('/')[0]
	//params = _url.split('/')[1]
	params = _url.replace(_url.split('/')[0],'')

	console.log(_url)
	console.log('ROUTE KEY IS : ' + routeKey);
	if (x_actions[routeKey] === undefined){x_log('Invalid Action Route..',1); return;}
	
	action_nav = x_actions[routeKey].x_go
	action_url = x_actions[routeKey].x_do
	if (params !== '') {action_url += params} 
	else {if (!(action_url.endsWith('/'))) {action_url += '/'}}
	

	if (x_actions[routeKey].x_act === 'post'){
		const _form = document.getElementById(_formname);
		x_post(_form, action_url,action_nav); 
	}
	if (x_actions[routeKey].x_act === 'del'){
		x_del(action_url,action_nav); 
	}
}

function x_post(_form, _url, _nav){	
	formdata = getFormData($(_form));
	console.log (formdata);
	
	$.ajax({
      type: "POST",
	  contentType: "application/json; charset=utf-8",
	  headers: {"x-ses": JSON.stringify(session_info.user)},
      url: _url,
      data: formdata
    }).done(function (data) {
		console.log(data);
		if (data.success === false){
			alert('Invalid credentials');
		}
		else{
			//console.log('dynamically calling ' + _nav + ' with ' + data._id);
			console.log('Initial NAV IS : ' + _nav);
			if (data !== undefined){_nav = _nav.replace(":ID", "/" + data._id);}
			console.log('Final NAV TO : ' + _nav);
			x_nav(_nav);
		}
    });
	
}

function x_del(_url, _nav){
	if (confirm('Are you sure you want to delete this item?')){
		$.ajax({
		  type: "DELETE",
		  contentType: "application/json; charset=utf-8",
		  url: _url
		}).done(function (data) {
		    console.log(data);
			if (data !== undefined){_nav = _nav.replace(":ID", "/" + data._id);}
			x_nav(_nav);

			/*
			if (data === "OK"){
				x_nav(_nav);
			}
			else{
				x_nav(_nav);
			}
			*/
			
		});
	}
}

function x_getJSON(url, success){
	$.ajax({
	  dataType: "json",
	  url: url,
	  headers: {"x-ses": JSON.stringify(session_info.user)},
	  success: success
	});	
}

function x_postJSON(url, jdata, success){
	$.ajax({
	  type: "POST",
	  headers: {"x-ses": JSON.stringify(session_info.user)},
	  url: url,
	  dataType: "json",
	  contentType: "application/json; charset=utf-8",
	  data: JSON.stringify(jdata),
	  success: success
	});	
}
 
//ReadMore for Multi-selection form data conversion
//https://shawnwang-dev.medium.com/post-arbitrary-json-data-dynamic-form-to-fastapi-using-ajax-84e537ce692b
function getFormData($form) {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};
	$.map(unindexed_array, function(n,i){
		console.log (i);
		indexed_array[n['name']] = n['value']
	});
	
	jsonString = JSON.stringify(indexed_array);
	return jsonString
}

//loaded_scripts = []
function loadScript(scriptSource){
	//if (loaded_scripts.indexOf(scriptSource) === -1) {
		var script = document.createElement('script');
		script.src = scriptSource;
		script.async = false;
		document.body.appendChild(script);
		//loaded_scripts.push(scriptSource);
	//}
	console.log('Loaded sript : ' + scriptSource);
}

// https://stackoverflow.com/questions/1293367/how-to-detect-if-javascript-files-are-loaded
// Great example of loading multiple scripts and then calling a call back function.
// Used in rehab - cv posenet loads.
// Also see here for JQeury way - https://stackoverflow.com/questions/29375510/how-to-know-if-a-javascript-script-was-loaded

function checkExtScript(url){
	var existingScript = document.querySelectorAll("script[src='" + url + "']");
	if (existingScript.length === 0) return false; 
	else return true;
}

function loadExtScript(path, callback) {

    var done = false;
    var scr = document.createElement('script');

    scr.onload = handleLoad;
    scr.onreadystatechange = handleReadyStateChange;
    scr.onerror = handleError;
    scr.src = path;
    document.body.appendChild(scr);

    function handleLoad() {
        if (!done) {
            done = true;
            callback(path, "ok");
        }
    }

    function handleReadyStateChange() {
        var state;

        if (!done) {
            state = scr.readyState;
            if (state === "complete") {
                handleLoad();
            }
        }
    }
    function handleError() {
        if (!done) {
            done = true;
            callback(path, "error");
        }
    }
}

function loadExtScripts(list, i, callback)
{
	if (checkExtScript(list[i])) {
		if(i < list.length-1)
		{
			loadExtScripts(list, i+1, callback);  
		}
		else
		{
			callback();
		}
	}
	else {
		loadExtScript(list[i], function()
		{
			if(i < list.length-1)
			{
				loadExtScripts(list, i+1, callback);  
			}
			else
			{
				callback();
			}
		})
	}
    
}


window.addEventListener('popstate', onPopState);

function onPopState(e) {
    let state = e.state;
    if (state !== null) {x_load(state);}
    else {history.back();}
}

function x_log(s,f){
	if (f <= debugLevel) console.log(s);
}

function clear_state(){
	if (window.speechSynthesis.speaking) {
		//console.error("speechSynthesis.speaking");
		//return;
		window.speechSynthesis.cancel();
	}	
}