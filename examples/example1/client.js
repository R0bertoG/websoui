var wsclient = function(){
	var api = {}
	////////////////////////////////////////////////////////////////
	var mapping_HTML_type_to_function = {};
	mapping_HTML_type_to_function["SPAN"] = function(span, data){
		while(span.firstChild){
			span.removeChild(span.firstChild);
		};
		txt = document.createTextNode(data);
		span.appendChild(txt);
	};
	mapping_HTML_type_to_function["TEXTAREA"] = function(textarea, data){
		textarea.value = data;
	};
	mapping_HTML_type_to_function["INPUT"] = function(inputElement, data){
		inputElement.value = data;
	};
	mapping_HTML_type_to_function["CANVAS"] = function(canvas, image){
		var image_obj = new Image();
		image_obj.onload = function(){
			var context = canvas.getContext('2d');
			context.drawImage(image_obj, 0, 0, canvas.width, canvas.height);
		};
		console.log(image)
		image_obj.src = "data:image/png;base64," + image; //+ images_objects[image_number]["image"];
	};
	////////////////////////////////////////////////////////////////
	api["get_mapping_HTML_type_to_function"] = function(){
		return mapping_HTML_type_to_function;
	};
	api["set_mapping_HTML_type_to_function"] = function(new_mapping){
		mapping_HTML_type_to_function = new_mapping;
	};
	////////////////////////////////////////////////////////////////
	var mapping_ID_to_function = {};
	api["get_mapping_ID_to_function"] = function(){
		return mapping_ID_to_function;
	};
	api["set_mapping_ID_to_function"] = function(new_mapping){
		mapping_ID_to_function = new_mapping;
	};
	////////////////////////////////////////////////////////////////
	var message_handler = function(event){
		var obj = JSON.parse( event.data);
		for (var key in obj){
			console.log(key, obj[key]);
			if (key in mapping_ID_to_function){
				mapping_ID_to_function[key](event.data);
				return;
			};
			try{
	    			var element = document.getElementById(key);
				var element_type = element.nodeName;
			}catch(err){
				return;
			};
			console.log("element type: ", element_type);
			if (element_type in mapping_HTML_type_to_function){
				mapping_HTML_type_to_function[element_type](element, obj[key]);
			}else{
				console.log('received data directed to an unexisting processor.');
			};
		};
	};
	////////////////////////////////////////////////////////////////
	api['send_message_to_server'] = function(msg){
		console.log('Impossible to send message to server, there is not connection.');
	};
	////////////////////////////////////////////////////////////////
	api['start_connection'] = function(websocket_uri){

        	var ws = new WebSocket(websocket_uri);
        	ws.onmessage = function(event) {
			message_handler(event);
		};

		ws.onopen = function(event){
			api['send_message_to_server'] = function(msg){
				ws.send(msg);
			};
		};
	};
	////////////////////////////////////////////////////////////////
	return api;

}();

//wsclient.start_connection('ws://127.0.0.1:5678/');
/*
var f = function(data){
	console.log(data);
};
d = wsclient.get_mapping_ID_to_function()
d["atextfield"]=f;

wsclient.set_mapping_ID_to_function(d);

wsclient.send_message_to_server("world")
*/

