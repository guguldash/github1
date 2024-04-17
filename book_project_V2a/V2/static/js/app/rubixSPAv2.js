class RubixCore {
  #_debug = true;
  get debug() {return this.#_debug;}
  set debug(val) {this.#_debug = val;}  

  #_version = '';
  get ver() {return this.#_version;}
  set ver(val) {this.#_version = val;}  
  
  curr_ses = {"user":{}}
  curr_page;

  init(){
	  //during app init, find the device type - web,mob,tab, browser - edge,chrome,safari etc
	  //this also defines capabilities of the device - do a checkFeature() - don't check all during load.
  }

  nav_page(p_page,p_params = ''){
	//Add history tracking and call load_page
	this.load_page(p_page,p_params)
  }
  
  load_page(p_page,p_params = ''){
	var url = navMap[p_page];
	var _page = new RubixPage();
	_page.params = p_params;
	$.getScript(url);
	
	//$.getScript(url,function(){
	//	_app.curr_page.params = p_params
	//});		
  }
  
  log(s){
	if (this.#_debug) console.log(s);
  }

  msg(s){
	if (this.#_debug) alert(s);
  }
  
  get(url, success){
	$.ajax({
	  dataType: "json",
	  url: url,
	  headers: {"x-ses": JSON.stringify(this.curr_ses.user)},
	  success: success
	});	
  }
  
  post(url,jdata, success){
	$.ajax({
		  type: "POST",
		  headers: {"x-ses": JSON.stringify(this.curr_ses.user)},
		  url: url,
		  dataType: "json",
		  contentType: "application/json; charset=utf-8",
		  //data: JSON.stringify(jdata),
		  data: jdata,
		  success: success
		});	
  }

  del(url,success){
	if (confirm('Are you sure you want to delete this item?')){
		$.ajax({
		  type: "DELETE",
		  headers: {"x-ses": JSON.stringify(this.curr_ses.user)},
		  url: url,
		  contentType: "application/json; charset=utf-8",
		  success: success
		});	
	}
  }
  
  form_json($form) {
	var unindexed_array = $form.serializeArray();
	var indexed_array = {};
	$.map(unindexed_array, function(n,i){
		indexed_array[n['name']] = n['value']
	});
	
	var jsonString = JSON.stringify(indexed_array);
	return jsonString
  }

  post_form($form,url,success){
	var dataJSON = _app.form_json($form);
	_app.post(url,dataJSON,success);
  }  
  
  bind_event(ctrl,evnt,action){
	$(ctrl).off().on(evnt,action);  
  }
}

class RubixPage {
	params = ''
	constructor(){
		_app.curr_page = this;
		this.api = {} //All API urls accessed in this page.
		this.views = {} //All inline views defined in this page.
		this.data = {} //All datasets for combos etc for this page.
		this.on = {} //All user actions/events bound on this page.
		
	}
	
	render_page(purl,json){    
		this.#render('p',purl,json,"x-body");
	}

	render_view(purl,json,div = "x-body"){  
		this.#render('s',purl,json,div);
	}

	#render(type,purl,json,div){  
		var env = nunjucks.configure([''], { autoescape: false });
		env.addGlobal('ses', _app.curr_ses);
		env.addGlobal('styles', _app.styles);
		try {
			//clear_state();
			if (type === 'p'){
				document.getElementById(div).innerHTML = env.render(purl, json);
			}

			if (type === 's'){
				document.getElementById(div).innerHTML = env.renderString(purl, json);
			}
		} catch (e) {
			_app.log(e,1);
		}
		this.#bind_sys_events();
	}

	display_table(tab_id){
		let table = new DataTable(tab_id,{ 
			pageLength: 9,
			layout : {topStart:null, topEnd:null},
			//layout : {topStart:null, topEnd:null, bottomStart:'info'},
			responsive: true,
			columnDefs: [{ width: 180, targets: -1 }],
			initComplete: function () {
			  var api = this.api();
			  $(tab_id).show();
			  api.columns.adjust();
			}
		});
		return table;
	}
	
	#bind_sys_events(){
		$("[data-nav]").off().on('click', function(e) {
			_app.load_page($(this).data('nav'))
			return false;
		});

		$("[data-enter]").off().on('keydown', function(e) {
			_app.log($(this).data('enter'))
			if (e.key === "Enter") {
				eval($(this).data('enter'));	
				return false;
			}
		});

		$("[data-change]").off().on('change', function(e) {
			if ($(this).data('change') === 'filter'){
				_cp.on.filter_list();
			}else if ($(this).data('change') === 'select'){
				_cp.sel_change(this);
			}
			else{
				//Do nothing for now.
			}
		});	
	}
	
	sel_init(ctrl,data,lbl='All',m_id,m_name,def=''){
		//On init, fill the options based on the data. Set the label and the def value.
		//If def = ':auto" then set the value from the hidden txtbox.
		$(ctrl).empty();
		$(ctrl).append('<option value="">' + lbl + '</option>');
		$.each(data, function () {
			_app.log(this);
			var option = $('<option/>');
			option.attr('value', this[m_id]).text(this[m_name]);
			$(ctrl).append(option);		 
		});
		if (def === ':auto'){
			this.sel_set(ctrl);
		}
		else{
			$(ctrl).val(def);			
		}
	}
	
	sel_set(ctrl){
		//On set of the hidden inputs, this sets the value of the select as well.
		var _prop = ($(ctrl).prop('id')).replace('sel_', '');
		var txt_id = '#txt_' + _prop + '_id';	
		$(ctrl).val($(txt_id).prop('value'))	
		return false;
	}

	sel_change(ctrl){
		//On change of the select, this sets the values of the hidden inputs
		var _prop = ($(ctrl).prop('id')).replace('sel_', '');
		var txt_id = '#txt_' + _prop + '_id';
		var txt_name = '#txt_' + _prop + '_name';		
		$(txt_id).val($(ctrl).prop('value'))	
		$(txt_name).val($(ctrl).prop('options')[$(ctrl).prop('selectedIndex')].innerHTML)
		return false;
	}

}
