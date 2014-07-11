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
function load_page(url, filter) {
	if (url[0] == "/") {
		$indicator = jQuery("#progress-indicator");
		$indicator.attr("style", "");
		$indicator.css("background-color", "white");
		$indicator.css("display", "block");
		$indicator.animate({width: "40%"}, 450);
		$indicator.css("background-color", "rgb(0, 180, 0)");
		
		var req = $.get(url, function(data) {
			var $realMain = jQuery("#main");
			var $data = jQuery("<div/>").html(data);
			var $main = $data.find("#main");
			var $title = $data.find("title");
			var reg = /#.+$/;
			window.document.title = $title.text();
			$indicator.animate({width: "100%"}, 250, function() {
				$indicator.attr("style", "");
			});
			$realMain.html($main.html());
			var m = url.match(reg);
			if (m !== null && m.length > 0 && m[0].length > 0) {
				jQuery.scrollTo(m[0]);
			} else {
				jQuery.scrollTo("body");
			}
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
		req.fail(function() {
			$indicator.css("background-color", "red");
			$indicator.animate({width: "100%"}, 700, function() {
				$indicator.attr("style", "");
			});
		});

		if (filter) {
			req.done(function() {
				jQuery("input[name=tags]").focus();
			});
		}
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

function fail(str) {
	function wrapper(data) {
		$result = jQuery("#result");
		$result.attr("class", "fail");
		$result.html("<strong class='error'>"+str+"</strong>");
		$result.css("display", "block");
		setTimeout("$result.fadeOut('slow')", 1500);
	}
	
	return wrapper;
}

function success(str, failStr) {
	function wrapper(data) {
		if (data.success) {
			$result = jQuery("#result");
			$result.attr("class", "okay");
			$result.html("<strong class='success'>"+str+"</strong>");
			$result.css("display", "block");
			setTimeout("$result.fadeOut('slow')", 1500);
			if (data.eid && data.result) {
				jQuery(data.eid).html(data.result);
			}
		} else {
			if (failStr) {
				fail(failStr)(data);
			} else {
				fail("Some kind of error")(data);
			}
		}
	}
	
	return wrapper;
}

function rmNote(id) {
	var result = $.post("/remove/", {"id": id}, success("Successfully removed note", "Failed to remove note"), "json");
	result.fail(fail("Failed to remove note"));
}

function ask(id, noteTitle) {
	var $dialog = jQuery(".remove-dialog");
	$dialog.css("display", "block");
	$dialog.html("<div class=\"close\">x</div><h3>Are you sure?</h3><p>You're trying to remove '"+noteTitle+"'</p><p class='btns'><div id=\"proceed\" class=\"btn-success\">Proceed</div><div id=\"do-not-delete\" class=\"btn-success\">Do not delete</div></p>");
	jQuery(".remove-dialog .close").click(function(e) {
		$dialog.fadeOut("slow");
	});
	jQuery(".remove-dialog #proceed").click(function(e) {
		rmNote(id);
		$dialog.fadeOut("slow");
		jQuery("#note-"+id).fadeOut("slow");
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

function edit(id, newTitle, newText, newTags, checked) {
	var result = $.post("/update/", {"id": id, "title": newTitle, "text": newText, "tags": newTags, "type": findChecked(), "checked": checked}, success("Successfully updated note", "Failed to update note"), "json");
	result.fail(fail("Failed to update note"));
}

function add(title, text, tags, todo) {
	var result = $.post("/addnote/", {"title": title, "text": text, "tags": tags, "todo": todo}, success("Successfully added note", "Failed to add note"), "json");
	result.fail(fail("Failed to add note"));
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
	var text = "", count = 0;
	var text_splitted = txt.split("\n");
	
	for (i = 0; i<text_splitted.length; i++) {
		count += 1;
		line = text_splitted[i];
		text += line.replace(/\t/gm, "&nbsp;&nbsp;&nbsp;&nbsp;");
		
		if (count < text_splitted.length) {
			if (line.search(/<.*?>$/) == -1) {
				text += "<br/>";
			}
			
			text += "\n";
		}
	}
	
	return text;
}

function anti_XSS(textarea) {
	var textarea_val = textarea.val();
	texarea_val = textarea_val.replace(
		/<[ \t]*script[ \t]*.*?>.*<[ \t]*\/[ \t]*script[ \t]*>/gim, "")
	textarea_val = textarea_val.replace(
		/<[ \t]*script[ \t]*.*?>.*/gim, "")
	textarea.val(textarea_val);
}

function preview() {
	var $preview = jQuery(".preview"),
	$text = $preview.find(".text"),
	$precode = $preview.find("pre code"),
	$pre = $preview.find("pre"),
	$title = jQuery("input[name=title]"),
	$textarea = jQuery("textarea[name=text]");
	$preview.find("h2").html("Preview");
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
		anti_XSS($textarea);
		if ($text.length < 1) {
			if ($pre.length > 0)
				$pre.remove();
			$preview.append("<p class='text'></p>");
		}
			if (jQuery("#is_warning").prop("checked")) {
				$preview.attr("class", "preview .warning");
			} else {
				$preview.attr("class", "preview .note");
			}
			$preview.find(".text").html(
				replaceNewLines($textarea.val())
			);
	}
	$preview.find("a > .title").html(escapeLtGt($title.val()));
	var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	var months = ['January', 'February', 'March', 'April', 'May', 'June', 'Jule', 'August', 'September', 'October', 'November', 'December'];
	var now = new Date(), weekday=days[now.getDay()], month=months[now.getMonth()];
	var $date = $preview.find(".date > time");
	$date.html(weekday + ", " + month + " " + addZero(now.getDate()) + " " + now.getFullYear() + " " + addZero(now.getHours()) + ":" +addZero(now.getMinutes()));
	$date.attr("datetime", now);
};

function preview1(d) {
	var $preview = jQuery(".preview"),
	$text = $preview.find(".text"),
	$title = jQuery("input[name=title]"),
	$textarea = jQuery("textarea[name=text]"),
	$pre = $preview.find("pre"),
	$precode = $pre.find("code");
	$preview.find("h2").html("Preview");
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
		anti_XSS($textarea);
		if ($text.length < 1) {
			if ($pre.length > 0)
				$pre.remove();
			$preview.append("<p class='text'></p>");
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
	$preview.find("a > .title").html(escapeLtGt($title.val()));
	var $date = $preview.find(".date > time");
	$date.attr("datetime", d);
	$date.html(d);
}

// @FILTER @HANDLEENTER @ENTER
// ==================================
// Enter key handling for filter page
// ==================================
function handleEnter(urlprefix) {
	jQuery(document).ready(function() {
		var $tags = jQuery("input[name=tags]");
		$tags.keypress(function(event) {
			if (event.which == 13) {
				load_page("/filter"+urlprefix+"/"+$tags.val());	
			}
		});
	});
}

// @KEY
// =============
// Key shortcuts
// =============
// @SHORTCUTS

jQuery(document).keypress(function(event) {
	if(!(jQuery(event.target).is("input, textarea"))) {
		switch(event.which) {
			case 49: // '1' key
			case 104: // 'h' key
				load_page('/');
				break;
			case 50: // '2' key
			case 97: // 'a' key
				load_page('/add/');
				break;
			case 51: // '3' key
			case 109: // 'm' key
				load_page('/manage/');
				break;
			case 52: // '4' key
			case 102: // 'f' key
				load_page('/filter/');
				break;
			case 115: // 's' key
				jQuery('input[name=q]').focus();
				break;
			case 35: // '#' key
				if (window.location.pathname.startsWith("/filter")) {
					jQuery.scrollTo("body");
					jQuery("input[name=tags]").focus();
				} else {
					load_page('/filter/', true);
				}
				break;
			case 110: // 'n' key
				jQuery('#next').trigger('click');
				break;
			case 112: // 'p' key
				jQuery('#previous').trigger('click');
				break;
			case 101: // 'e' key
				jQuery('.edit_button').trigger('click');
				break;
			default:
				break;
		}
	}
});

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

$(document).ready(function() {
	var $q = $("input[name=q]");
	$q.keypress(function(event) {
		if (event.which == 13) {
			load_page('/search/'+$q.val());
		}
	});
	
	$(window).on("popstate", function(event) {
		var state = event.originalEvent.state;
	    if (!state) {
			return;
		} else {
			var newDoc = document.open("text/html", "");
			newDoc.write(state.content);
			newDoc.close();
		}
	});
});

function PlaceReadMoreButtons() {
	jQuery(document).ready(function() {
		var $note = $("article");
		$note.each(function(i, e) {
			var $text = $(this).find(".text");
			var $snippet = $(this).find("pre");
			if (parseInt($text.css("height")) > 400) {
				$text.addClass("cut");
				var href = $(this).find("a").attr("href");
				$(this).append("<a href='"+href+"' onclick='load_page(\""+href+"\"); return false;'><div class='read-more-btn'>Continue reading</div></a>");
			} else if (parseInt($snippet.css("height")) > 210) {
				$snippet.addClass("cut");
				var href = $(this).find("a").attr("href");
				$(this).append("<a href='"+href+"' onclick='load_page(\""+href+"\"); return false;'><div class='read-more-btn'>Continue reading</div></a>");
			}
		});
	});
}

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

// @HIGHLIGHT
// ==============
// Highlight code
// ==============
hljs.configure({tabReplace: '    '});
hljs.initHighlightingOnLoad();

// @USER @ACCOUNT
// =======================
// User account management
// =======================

function update_first_name(id, new_first_name) {
	var res = jQuery.post("/update-firstname/", {"id": id, "new_first_name": new_first_name}, success("First name updated", "#"), "json");
	res.error(fail("Some kind of error"));
}

function update_last_name(id, new_last_name) {
	var res = jQuery.post("/update-lastname/", {"id": id, "new_last_name": new_last_name}, success("Last name updated"), "json");
	res.error(fail("Some kind of error"));
}

function update_username(id, new_username) {
	var res = jQuery.post("/update-username/", {"id": id, "new_username": new_username}, function(data) {
			success("Username updated")(data);
			if (data.success) {
				document.title = new_username + "'s profile - Noter";
			}
		}, "json");
	res.error(fail("Some kind of error"));
}

function update_password(id, current_password, new_password, confirm_password) {
	var res = jQuery.post("/update-password/", {"id": id, "new_password": new_password, "current_password": current_password, "confirm_password": confirm_password}, success("Password updated"), "json");
	res.error(fail("Some kind of error"));
}
