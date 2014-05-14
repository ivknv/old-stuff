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
		$realMain = jQuery(".main");
		$realMain.css("background-color", "rgba(254, 254, 254, 0.95)");
		
		$.get(url, function(data) {
			var $data = jQuery("<div/>").html(data);
			var $main = $data.find(".main");
			var $realMain = jQuery(".main")
			var $title = $data.find("title");
			window.document.title = $title.text();
			$realMain.html($main.html());
			$realMain.css("background-color", "rgba(254, 254, 254, 1)");
			jQuery.scrollTo("body");
			var state = {
				url: url,
				title: $title.text(),
				content: data
			};
			history.pushState(state, state.title, url);
			jQuery("pre code").each(function(i, e) {
				hljs.highlightBlock(e);
			});
		}, "html");
	} else {
		window.href = url;
	}
}

function load_page2(url) {
	if (url[0] == "/") {
		$realMain = jQuery(".main");
		$realMain.css("background-color", "rgba(254, 254, 254, 0.95)");
		
		$.get(url, function(data) {
			var $data = jQuery("<div/>").html(data);
			var $main = $data.find(".main");
			var $title = $data.find("title");
			window.document.title = $title.text();
			$realMain.html($main.html());
			$realMain.css("background-color", "rgba(254, 254, 254, 1)");
			jQuery.scrollTo(".note");
			var state = {
				url: url,
				title: $title.text(),
				content: data
			};
			history.pushState(state, state.title, url);
			jQuery("pre code").each(function(i, e) {
				hljs.highlightBlock(e);
			});
		}, "html");
	} else {
		window.href = url;
	}
}


// @TAG @TAGS
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
	var $tagfield = jQuery("input[name=tags]");
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
	$tagfield.focus();
}

function getTags(id, text, title) {
	$.post("/suggestedtags/", {"id": id, "text": text, "title": title}, function(data) {
		var $stags = jQuery(".suggested-tags");
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
						$stags.append("<div class='tag-btn' onclick='placeTag(jQuery(this).html());' type='button'>"+tags[i]+"</div>");
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
			var $note = jQuery("#note-"+id);
			$note.fadeOut("slow");
			setTimeout('jQuery("#note-'+id+'").remove()', 1000);
			$result = jQuery("#result");
			$result.addClass("okay");
			$result.css("display", "block");
			$result.html("<strong class=\"success\">Succesfully removed</strong>");
			setTimeout('$result.fadeOut("slow")', 1500);
		}
		else
			fail();
	};
	var result = $.post("/remove/", {"id": id}, success, "json");
	result.fail(rmNote_fail);
}

function rmNote_fail() {
	$result = jQuery("#result");
	$result.addClass("fail");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to remove note</strong>");
	setTimeout('$result.fadeOut("slow")', 1500);
}

function ask(id, noteTitle) {
	var $dialog = jQuery(".remove-dialog");
	$dialog.css("display", "block");
	$dialog.html("<div class=\"close\">x</div><h3>Are you sure?</h3><p>You're trying to remove '"+noteTitle+"'</p><p class='btns'><div id=\"proceed\" class=\"btn-success\">Proceed</div><div id=\"do-not-delete\" class=\"btn-success\">Do not delete</div></p>");
	jQuery(".remove-dialog .close").click(function(e) {
		$dialog.fadeOut("slow");
	});
	jQuery(".remove-dialog #proceed").click(function(e) {
		rmNote(id, rmNote_fail);
		$dialog.fadeOut("slow")
	});
	jQuery(".remove-dialog #do-not-delete").click(function(e) {
		$dialog.fadeOut("slow");
	});
}

function findChecked() {
	var isNote = jQuery("#note").prop("checked"),
	isTodo = jQuery("#todo").prop("checked"),
	isSnippet = jQuery("#snippet").prop("checked"),
	isWarning = jQuery("#warning").prop("checked");
	if (isNote)
		return "n";
	else if (isTodo)
		return "t";
	else if (isSnippet)
		return "s";
	else if (isWarning)
		return "w";
	else
		return "Unknown";
}

function edit_success(data) {
	if (!(data.failed)) {
		$result = jQuery("#result");
		$result.addClass("okay");
		$result.css("display", "block");
		$result.html("<strong class=\"success\">Successfully updated note</strong>");
		setTimeout('$result.fadeOut("slow")', 1500);
	} else
		edit_fail();
}

function edit_fail() {
	$result = jQuery("#result");
	$result.addClass("fail");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to update note</strong>");
	setTimeout('$result.fadeOut("slow")', 1500);
}

function edit(id, newTitle, newText, newTags, checked) {
	var result = $.post("/update/", {"id": id, "title": newTitle, "text": newText, "tags": newTags, "type": findChecked(), "checked": checked}, edit_success, "json");
	result.fail(edit_fail);
}

function add_success(data) {
	if (!(data.failed)) {
		$result = jQuery("#result");
		$result.addClass("alert-success");
		$result.css("display", "block");
		$result.html("<strong class=\"success\">Note was successfully added</strong>");
		setTimeout('$result.fadeOut("slow")', 1500);
	} else
		add_fail();
}

function add_fail() {
	$result = jQuery("#result");
	$result.addClass("alert-danger");
	$result.css("display", "block");
	$result.html("<strong class=\"error\">Failed to add note</string>");
	setTimeout('$result.fadeOut("slow")', 1500);
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

function escapeLtGt(code) {
	return code.replace(/&/gm, "&amp;").replace(/</gm, "&lt;").replace(/>/gm, "&gt;");
}

function replaceNewLines(txt) {
	return txt.replace(/\n/gm, "<br/>").replace(/\t/gm, "&nbsp;&nbsp;&nbsp;&nbsp;")
}

function preview() {
	var $preview = jQuery(".preview"),
	$text = $preview.find(".text"),
	$precode = $preview.find("pre code"),
	$pre = $preview.find("pre"),
	$title = jQuery("input[name=title]"),
	$textarea = jQuery("textarea[name=text]");
	$preview.find("h2").html("Preview");
	$preview.find("a > .title").html($title.val());
	if (jQuery("#is_snippet").prop("checked")) {
		$preview.attr("class", "preview snippet");
		$text.remove();
		if ($pre.length < 1)
			$preview.append("<pre><code></code></pre>");
		$preview.find("pre code").each(function(i, e) { // Because elements should be refreshed
			jQuery(this).html(escapeLtGt($textarea.val()));
			hljs.highlightBlock(e);
		});
	} else {
		if ($text.length < 1) {
			if ($pre.length > 0)
				$pre.remove();
			$preview.append("<p class='text'></p>")
		}
			if (jQuery("#is_warning").prop("checked")) {
				$preview.attr("class", "preview warning");
			} else {
				$preview.attr("class", "preview note");
			}
			$preview.find(".text").html(
				replaceNewLines($textarea.val())
			);
	}
	$preview.find("a > .title").html(escapeLtGt($title.val()))
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	var months = ['January', 'February', 'March', 'April', 'May', 'June', 'Jule', 'August', 'September', 'October', 'November', 'December'];
	var now = new Date(), weekday=days[now.getDay()], month=months[now.getMonth()];
	jQuery(".preview .date").html(weekday + ", " + month + " " + addZero(now.getDate()) + " " + now.getFullYear() + " " + addZero(now.getHours()) + ":" +addZero(now.getMinutes()));
};

function preview1(d) {
	var $preview = jQuery(".preview"),
	$text = $preview.find(".text"),
	$title = jQuery("input[name=title]"),
	$textarea = jQuery("textarea[name=text]"),
	$pre = $preview.find("pre"),
	$precode = $pre.find("code");
	$preview.find("h2").html("Preview");
	$preview.find("a > .title").html($title.val());
	if (jQuery("#snippet").prop("checked")) {
		$preview.attr("class", "preview snippet");
		if ($text.length > 0)
			$text.remove();
		if ($pre.length < 1)
			$preview.append("<pre><code></code></pre>");
		$preview.find("pre code").each(function(i, e) {
			jQuery(this).html(escapeLtGt($textarea.val()));
			hljs.highlightBlock(e);
		});
	} else {
		if ($text.length < 1) {
			if ($pre.length > 0)
				$pre.remove();
			$preview.append("<p class='text'></p>")
		}
			if (jQuery("#warning").prop("checked")) {
				$preview.attr("class", "preview warning");
			} else {
				$preview.attr("class", "preview note");
			}
			$preview.find(".text").html(
				replaceNewLines($textarea.val())
			);
	}
	$preview.find("a > .title").html(escapeLtGt($title.val()))
	$preview.find(".date").html(d);
}

// @FILTER
// ==================================
// Enter key handling for filter page
// ==================================
function handleEnter() {
	jQuery(document).ready(function() {
		var $tags = jQuery("input[name=tags]");
		$tags.keypress(function(event) {
			if (event.which == 13) {
				load_page("/filter/"+$tags.val()+"/1/");	
			}
		});
	});
}

// @TAB @TTAB
// =============================
// Tab key handling for textarea
// =============================

function enableTab(id) {
    var el = document.getElementById(id);
    el.onkeydown = function(e) {
        if (e.keyCode === 9) { // tab was pressed

            // get caret position/selection
            var val = this.value,
                start = this.selectionStart,
                end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = val.substring(0, start) + '\t' + val.substring(end);

            // put caret at right position again
            this.selectionStart = this.selectionEnd = start + 1;

            // prevent the focus lose
            return false;

        }
    };
}

// @READY
// =======
// On load
// =======
// @ONREADY

/*function antiEscapeLtGt(code) {
	return code.replace(/&amp;/gm, "&").replace(/&lt;/gm, "<").replace(/&gt;/gm, ">").replace(/&quot;/gm, '"').replace(/&#39/gm, "");
}*/

function antiEscapeLtGt2(code) {
	return code.replace(/&lt;/gm, "<").replace(/&gt;/gm, ">").replace(/&amp;lt;/gm, "&lt;").replace(/&amp;gt;/gm, "&gt;").replace(/&amp;/gm, "&");
}

function onLoad() {
	// Fixes for various browsers
	jQuery(document).ready(function() {
		var usag = navigator.userAgent.toLowerCase();
			if (usag.indexOf("chrome") > -1 || usag.indexOf("applewebkit") > -1 || usag.indexOf("presto") > -1) {
			jQuery(".filter-btn").css("line-height", "1.5");
			jQuery(".search-btn").css("line-height", "1.75");
			jQuery(".input-field").css("margin-top", "4px");
			jQuery(".label").css("padding-bottom", "3px");
		}
	
		// Make text normal
		jQuery("article .text").each(function() {
			jQuery(this).html(antiEscapeLtGt2(jQuery(this).html()));
		});
	});
}

// Highlight code
hljs.configure({tabReplace: '    '});
hljs.initHighlightingOnLoad();
