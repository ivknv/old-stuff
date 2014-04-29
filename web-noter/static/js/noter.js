// @CSRF
// ====
// CSRF
// ====
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// @PAGELOAD @PLA @PAGE
// ===================
// Page load with AJAX
// ===================
function load_page(url) {
	if (url[0] == "/") {
		$.get(url, function(data) {
			var $data = $("<div/>").html(data);
			var $main = $data.find(".main");
			var $title = $data.find("title");
			$(".main").css("opacity", "0.5");
			$(".main").html($main.html());
			$(".main").css("opacity", "1");
			window.document.title = $title.text();
			$.scrollTo("body");
			var state = {
				url: url,
				title: $title.text(),
				content: data
			};
			console.log($main.html());
			history.pushState(state, state.title, url);
		}, "html");
	} else {
		window.href = url;
	}
}

// @TAG
// ==============
// Tag suggesting
// ==============

Array.prototype.contains = function(v) {
    for(var i = 0; i < this.length; i++) {
        if(this[i] === v) return true;
    }
    return false;
};

Array.prototype.unique = function() {
    var arr = [];
    for(var i = 0; i < this.length; i++) {
        if(!arr.contains(this[i])) {
            arr.push(this[i]);
        }
    }
    return arr; 
}

function placeTag(tag) {
	var $tagfield = $("input[name=tags]");
	var newval = $tagfield.val();
	if (newval[-1] == " ")
		newval = newval.slice(0, -1) + ", " + tag;
	else if (newval[-1] == ",")
		newval = newval + " " + tag;
	else if (newval)
		newval = newval + ", " + tag;
	else
		newval = tag;
	$tagfield.val(newval);
}

function getTags(id, text, title) {
	$.post("/suggestedtags/", {"id": id, "text": text, "title": title}, function(data) {
		var $stags = $(".suggested-tags");
		var u = [];
		$stags.empty();
		$.each(data.top3, function(i) {
			if (data.top3[i][1][1][2].length > 0)
				var tags = data.top3[i][1][1][2];
				
				$.each(tags, function(i) {
					if (tags[i][0] == " ")
						tags[i][0] = "";
					if (!u.contains(tags[i])) {
						u.push(tags[i]);
						console.log(u);
						$stags.append("<button class='btn tag-btn' onclick='placeTag($(this).html());'>"+tags[i]+"</button>");
					}
				});
		});
	}, "json");
}

// @MANAGE
// ===============
// Note management
// ===============

function rmNote(id) {
	var success=function (data) {
		if (data["success"]) {
			var $note = $("#note-"+id);
			$note.fadeOut("slow");
			setTimeout('$("#note-'+id+'").remove()', 1000);
			$result = $("#result");
			$result.addClass("alert-success");
			$result.css("display", "block");
			$result.html("<strong class=\"success\">Note was succesfully removed</strong>");
			setTimeout('$result.fadeOut("slow")', 1500);
		}
		else
			fail();
	};
	var result = $.post("/remove/", {"id": id}, success, "json");
	result.fail(rmNote_fail);
}

function rmNote_fail() {
	$result = $("#result");
	$result.addClass("alert-danger");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to remove note</strong>");
	setTimeout('$result.fadeOut("slow")', 1500);
}

function ask(id, noteTitle) {
	$dialog = $(".remove-dialog");
	$dialog.css("display", "block");
	$dialog.html("<button class=\"close\" aria-hidden=\"true\" data-dismiss=\"alert\" type=\"button\">x</button><h3>Are you sure?</h3><p>You're trying to remove '"+noteTitle+"'</p><p><button id=\"proceed\" class=\"btn\">Proceed</button><button id=\"do-not-delete\" class=\"btn\">Do not delete</button></p>");
	$(".remove-dialog .close").click(function(e) {
		$dialog.fadeOut("slow");
	});
	$(".remove-dialog #proceed").click(function(e) {
		rmNote(id, rmNote_fail);
		$dialog.fadeOut("slow")
	});
	$(".remove-dialog #do-not-delete").click(function(e) {
		$dialog.fadeOut("slow");
	});
}

function edit_success(data) {
	if (!(data.failed)) {
		var $result = $("#result");
		$result.addClass("alert-success");
		$result.css("display", "block");
		$result.html("<strong class=\"success\">Note was successfully updated</strong>");
		setTimeout('$("#result").fadeOut("slow")', 1500);
	} else
		edit_fail();
}

function edit_fail() {
	var $result = $("#result");
	$result.addClass("alert-danger");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to update note</strong>");
	setTimeout('$("#result").fadeOut("slow")', 1500);
}

function edit(id, newTitle, newText, newTags, todo, checked) {
	var result = $.post("/update/", {"id": id, "title": newTitle, "text": newText, "tags": newTags, "todo": todo, "checked": checked}, edit_success, "json");
	result.fail(edit_fail);
}

function add_success(data) {
	if (!(data.failed)) {
		var $result = $("#result");
		$result.addClass("alert-success");
		$result.css("display", "block");
		$result.html("<strong class=\"success\">Note was successfully added</strong>");
		setTimeout('$("#result").fadeOut("slow")', 1500);
	} else
		add_fail();
}

function add_fail() {
	var $result = $("#result");
	$result.addClass("alert-danger");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to add note</string>");
	setTimeout('$("#result").fadeOut("slow")', 1500);
}

function add(title, text, tags, todo) {
	var result = $.post("/addnote/", {"title": title, "text": text, "tags": tags, "todo": todo}, add_success, "json");
	result.fail(add_fail);
}

// @PREVIEW
// ============
// Note preview
// ============

function addZero(i) {
	return i>=0 && i<10 ? ""+0+i : ""+i;
};

function preview() {
	$(".preview h2").html("Preview");
	$(".preview a > .title").html($(".col-6-md div input[name=title]").val());
	$(".preview .text").html($(".col-6-md div textarea[name=text]").val().replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;"));
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	var months = ['January', 'February', 'March', 'April', 'May', 'June', 'Jule', 'August', 'September', 'October', 'November', 'December'];
	var now = new Date(), weekday=days[now.getDay()], month=months[now.getMonth()];
	$(".preview .date").html(weekday + ", " + month + " " + addZero(now.getDate()) + " " + now.getFullYear() + " " + addZero(now.getHours()) + ":" +addZero(now.getMinutes()));
};
function preview1(d) {
	$(".preview h2").html("Preview");
	$(".preview a > .title").html($(".col-6-md div input[name=title]").val());
	$(".preview .text").html($(".col-6-md div textarea[name=text]").val().replace(/\n/g, "<br/>").replace(/ /g, "&nbsp;"));
	$(".preview .date").html(d);
};

// @FILTER
// ==================================
// Enter key handling for filter page
// ==================================
function handleEnter() {
	$(document).ready(function() {
		var $tags = $("input[name=tags]");
		$tags.keypress(function(event) {
			if (event.which == 13) {
				load_page("/filter/"+$tags.val()+"/1/");	
			}
		});
	});
}
