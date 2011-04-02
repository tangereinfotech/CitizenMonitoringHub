// Inserts shortcut buttons after all of the following:
//     <input type="text" class="vDateField">
//     <input type="text" class="vTimeField">

var DateTimeHandler = {
    calendars: [],
    calendarInputs: [],
    clockInputs: [],
    calendarDivName1: 'calendarbox', // name of calendar <div> that gets toggled
    calendarDivName2: 'calendarin',  // name of <div> that contains calendar
    calendarLinkName: 'calendarlink',// name of the link that is used to toggle
    clockDivName: 'clockbox',        // name of clock <div> that gets toggled
    clockLinkName: 'clocklink',      // name of the link that is used to toggle
    shortCutsClass: 'datetimeshortcuts', // class of the clock and cal shortcuts
    admin_media_prefix: '',
    init: function(date_class, time_class) {
        // Get admin_media_prefix by grabbing it off the window object. It's
        // set in the admin/base.html template, so if it's not there, someone's
        // overridden the template. In that case, we'll set a clearly-invalid
        // value in the hopes that someone will examine HTTP requests and see it.
        var time_re = new RegExp (time_class);
        var date_re = new RegExp (date_class);

        if (window.__admin_media_prefix__ != undefined) {
            DateTimeHandler.admin_media_prefix = window.__admin_media_prefix__;
        } else {
            DateTimeHandler.admin_media_prefix = '/missing-admin-media-prefix/';
        }

        var inputs = document.getElementsByTagName('input');
        for (i=0; i<inputs.length; i++) {
            var inp = inputs[i];
            if (inp.getAttribute('type') == 'text' && inp.className.match (time_re)) {
                DateTimeHandler.addClock(inp);
            }
            else if (inp.getAttribute('type') == 'text' && inp.className.match(date_re)) {
                DateTimeHandler.addCalendar(inp);
            }
        }
    },
    // Add clock widget to a given field
    addClock: function(inp) {
        var num = DateTimeHandler.clockInputs.length;
        DateTimeHandler.clockInputs[num] = inp;

        // Shortcut links (clock icon and "Now" link)
        var shortcuts_span = document.createElement('span');
        shortcuts_span.className = DateTimeHandler.shortCutsClass;
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        var now_link = document.createElement('a');
        now_link.setAttribute('href', "javascript:DateTimeHandler.handleClockQuicklink(" + num + ", new Date().strftime('" + get_format('TIME_INPUT_FORMATS')[0] + "'));");
        now_link.appendChild(document.createTextNode(gettext('Now')));
        var clock_link = document.createElement('a');
        clock_link.setAttribute('href', 'javascript:DateTimeHandler.openClock(' + num + ');');
        clock_link.id = DateTimeHandler.clockLinkName + num;
        quickElement('img', clock_link, '', 'src', DateTimeHandler.admin_media_prefix + 'img/admin/icon_clock.gif', 'alt', gettext('Clock'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        shortcuts_span.appendChild(now_link);
        shortcuts_span.appendChild(document.createTextNode('\240|\240'));
        shortcuts_span.appendChild(clock_link);

        // Create clock link div
        //
        // Markup looks like:
        // <div id="clockbox1" class="clockbox module">
        //     <h2>Choose a time</h2>
        //     <ul class="timelist">
        //         <li><a href="#">Now</a></li>
        //         <li><a href="#">Midnight</a></li>
        //         <li><a href="#">6 a.m.</a></li>
        //         <li><a href="#">Noon</a></li>
        //     </ul>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>

        var clock_box = document.createElement('div');
        clock_box.style.display = 'none';
        clock_box.style.position = 'absolute';
        clock_box.className = 'clockbox module';
        clock_box.setAttribute('id', DateTimeHandler.clockDivName + num);
        document.body.appendChild(clock_box);
        addEvent(clock_box, 'click', DateTimeHandler.cancelEventPropagation);

        quickElement('h2', clock_box, gettext('Choose a time'));
        time_list = quickElement('ul', clock_box, '');
        time_list.className = 'timelist';
        time_format = get_format('TIME_INPUT_FORMATS')[0];
        quickElement("a", quickElement("li", time_list, ""), gettext("Now"), "href", "javascript:DateTimeHandler.handleClockQuicklink(" + num + ", new Date().strftime('" + time_format + "'));");
        quickElement("a", quickElement("li", time_list, ""), gettext("Midnight"), "href", "javascript:DateTimeHandler.handleClockQuicklink(" + num + ", new Date(1970,1,1,0,0,0,0).strftime('" + time_format + "'));");
        quickElement("a", quickElement("li", time_list, ""), gettext("6 a.m."), "href", "javascript:DateTimeHandler.handleClockQuicklink(" + num + ", new Date(1970,1,1,6,0,0,0).strftime('" + time_format + "'));");
        quickElement("a", quickElement("li", time_list, ""), gettext("Noon"), "href", "javascript:DateTimeHandler.handleClockQuicklink(" + num + ", new Date(1970,1,1,12,0,0,0).strftime('" + time_format + "'));");

        cancel_p = quickElement('p', clock_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeHandler.dismissClock(' + num + ');');
    },
    openClock: function(num) {
        var clock_box = document.getElementById(DateTimeHandler.clockDivName+num)
        var clock_link = document.getElementById(DateTimeHandler.clockLinkName+num)
    
        // Recalculate the clockbox position
        // is it left-to-right or right-to-left layout ?
        if (getStyle(document.body,'direction')!='rtl') {
            clock_box.style.left = findPosX(clock_link) + 17 + 'px';
        }
        else {
            // since style's width is in em, it'd be tough to calculate
            // px value of it. let's use an estimated px for now
            // TODO: IE returns wrong value for findPosX when in rtl mode
            //       (it returns as it was left aligned), needs to be fixed.
            clock_box.style.left = findPosX(clock_link) - 110 + 'px';
        }
        clock_box.style.top = findPosY(clock_link) - 30 + 'px';
    
        // Show the clock box
        clock_box.style.display = 'block';
        addEvent(window.document, 'click', function() { DateTimeHandler.dismissClock(num); return true; });
    },
    dismissClock: function(num) {
       document.getElementById(DateTimeHandler.clockDivName + num).style.display = 'none';
       window.document.onclick = null;
    },
    handleClockQuicklink: function(num, val) {
       DateTimeHandler.clockInputs[num].value = val;
       DateTimeHandler.clockInputs[num].focus();
       DateTimeHandler.dismissClock(num);
    },
    // Add calendar widget to a given field.
    addCalendar: function(inp) {
        var num = DateTimeHandler.calendars.length;

        DateTimeHandler.calendarInputs[num] = inp;

        // Shortcut links (calendar icon and "Today" link)
        var shortcuts_span = document.createElement('span');
        shortcuts_span.className = DateTimeHandler.shortCutsClass;
        inp.parentNode.insertBefore(shortcuts_span, inp.nextSibling);
        var today_link = document.createElement('a');
        today_link.setAttribute('href', 'javascript:DateTimeHandler.handleCalendarQuickLink(' + num + ', 0);');
        today_link.appendChild(document.createTextNode(gettext('Today')));
        var cal_link = document.createElement('a');
        cal_link.setAttribute('href', 'javascript:DateTimeHandler.openCalendar(' + num + ');');
        cal_link.id = DateTimeHandler.calendarLinkName + num;
        quickElement('img', cal_link, '', 'src', DateTimeHandler.admin_media_prefix + 'img/admin/icon_calendar.gif', 'alt', gettext('Calendar'));
        shortcuts_span.appendChild(document.createTextNode('\240'));
        shortcuts_span.appendChild(today_link);
        shortcuts_span.appendChild(document.createTextNode('\240|\240'));
        shortcuts_span.appendChild(cal_link);

        // Create calendarbox div.
        //
        // Markup looks like:
        //
        // <div id="calendarbox3" class="calendarbox module">
        //     <h2>
        //           <a href="#" class="link-previous">&lsaquo;</a>
        //           <a href="#" class="link-next">&rsaquo;</a> February 2003
        //     </h2>
        //     <div class="calendar" id="calendarin3">
        //         <!-- (cal) -->
        //     </div>
        //     <div class="calendar-shortcuts">
        //          <a href="#">Yesterday</a> | <a href="#">Today</a> | <a href="#">Tomorrow</a>
        //     </div>
        //     <p class="calendar-cancel"><a href="#">Cancel</a></p>
        // </div>
        var cal_box = document.createElement('div');
        cal_box.style.display = 'none';
        cal_box.style.position = 'absolute';
        cal_box.className = 'calendarbox module';
        cal_box.setAttribute('id', DateTimeHandler.calendarDivName1 + num);
        document.body.appendChild(cal_box);
        addEvent(cal_box, 'click', DateTimeHandler.cancelEventPropagation);

        // next-prev links
        var cal_nav = quickElement('div', cal_box, '');
        var cal_nav_prev = quickElement('a', cal_nav, '<', 'href', 'javascript:DateTimeHandler.drawPrev('+num+');');
        cal_nav_prev.className = 'calendarnav-previous';
        var cal_nav_next = quickElement('a', cal_nav, '>', 'href', 'javascript:DateTimeHandler.drawNext('+num+');');
        cal_nav_next.className = 'calendarnav-next';

        // main box
        var cal_main = quickElement('div', cal_box, '', 'id', DateTimeHandler.calendarDivName2 + num);
        cal_main.className = 'calendar';
        DateTimeHandler.calendars[num] = new Calendar(DateTimeHandler.calendarDivName2 + num, DateTimeHandler.handleCalendarCallback(num));
        DateTimeHandler.calendars[num].drawCurrent();

        // calendar shortcuts
        var shortcuts = quickElement('div', cal_box, '');
        shortcuts.className = 'calendar-shortcuts';
        quickElement('a', shortcuts, gettext('Yesterday'), 'href', 'javascript:DateTimeHandler.handleCalendarQuickLink(' + num + ', -1);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Today'), 'href', 'javascript:DateTimeHandler.handleCalendarQuickLink(' + num + ', 0);');
        shortcuts.appendChild(document.createTextNode('\240|\240'));
        quickElement('a', shortcuts, gettext('Tomorrow'), 'href', 'javascript:DateTimeHandler.handleCalendarQuickLink(' + num + ', +1);');

        // cancel bar
        var cancel_p = quickElement('p', cal_box, '');
        cancel_p.className = 'calendar-cancel';
        quickElement('a', cancel_p, gettext('Cancel'), 'href', 'javascript:DateTimeHandler.dismissCalendar(' + num + ');');
    },
    openCalendar: function(num) {
        var cal_box = document.getElementById(DateTimeHandler.calendarDivName1+num)
        var cal_link = document.getElementById(DateTimeHandler.calendarLinkName+num)
        var inp = DateTimeHandler.calendarInputs[num];

        // Determine if the current value in the input has a valid date.
        // If so, draw the calendar with that date's year and month.
        if (inp.value) {
            var date_parts = inp.value.split('-');
            var year = date_parts[0];
            var month = parseFloat(date_parts[1]);
            if (year.match(/\d\d\d\d/) && month >= 1 && month <= 12) {
                DateTimeHandler.calendars[num].drawDate(month, year);
            }
        }

        // Recalculate the clockbox position
        // is it left-to-right or right-to-left layout ?
        if (getStyle(document.body,'direction')!='rtl') {
            cal_box.style.left = findPosX(cal_link) + 17 + 'px';
        }
        else {
            // since style's width is in em, it'd be tough to calculate
            // px value of it. let's use an estimated px for now
            // TODO: IE returns wrong value for findPosX when in rtl mode
            //       (it returns as it was left aligned), needs to be fixed.
            cal_box.style.left = findPosX(cal_link) - 180 + 'px';
        }
        cal_box.style.top = findPosY(cal_link) - 75 + 'px';
    
        cal_box.style.display = 'block';
        addEvent(window.document, 'click', function() { DateTimeHandler.dismissCalendar(num); return true; });
    },
    dismissCalendar: function(num) {
        document.getElementById(DateTimeHandler.calendarDivName1+num).style.display = 'none';
        window.document.onclick = null;
    },
    drawPrev: function(num) {
        DateTimeHandler.calendars[num].drawPreviousMonth();
    },
    drawNext: function(num) {
        DateTimeHandler.calendars[num].drawNextMonth();
    },
    handleCalendarCallback: function(num) {
        format = get_format('DATE_INPUT_FORMATS')[0];
        // the format needs to be escaped a little
        format = format.replace('\\', '\\\\');
        format = format.replace('\r', '\\r');
        format = format.replace('\n', '\\n');
        format = format.replace('\t', '\\t');
        format = format.replace("'", "\\'");
        return ["function(y, m, d) { DateTimeHandler.calendarInputs[",
               num,
               "].value = new Date(y, m-1, d).strftime('",
               format,
               "');DateTimeHandler.calendarInputs[",
               num,
               "].focus();document.getElementById(DateTimeHandler.calendarDivName1+",
               num,
               ").style.display='none';}"].join('');
    },
    handleCalendarQuickLink: function(num, offset) {
       var d = new Date();
       d.setDate(d.getDate() + offset)
       DateTimeHandler.calendarInputs[num].value = d.strftime(get_format('DATE_INPUT_FORMATS')[0]);
       DateTimeHandler.calendarInputs[num].focus();
       DateTimeHandler.dismissCalendar(num);
    },
    cancelEventPropagation: function(e) {
        if (!e) e = window.event;
        e.cancelBubble = true;
        if (e.stopPropagation) e.stopPropagation();
    }
}

