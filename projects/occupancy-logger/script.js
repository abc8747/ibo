var starttime;
var loop;
var events = [];

$(document).ready(function() {
    function saveJSON(filename, jsonToWrite) {
        const blob = new Blob([jsonToWrite], { type: "text/json" });
        const link = document.createElement("a");
    
        link.download = filename;
        link.href = window.URL.createObjectURL(blob);
        link.dataset.downloadurl = ["text/json", link.download, link.href].join(":");
    
        const evt = new MouseEvent("click", {
            view: window,
            bubbles: true,
            cancelable: true,
        });
    
        link.dispatchEvent(evt);
        link.remove()
    };

    function getSecElapsed() {
        return (Date.now() - starttime) / 1000;
    }

    function updateTimer() {
        $('#timer').html(`${Math.round(getSecElapsed())} s`)
    }

    function start() {
        if (loop === undefined) {
            $('#start').prop('disabled', true);
            $('#stop').prop('disabled', false);
            events = [];
            starttime = Date.now();
            loop = setInterval(updateTimer, 100);
        }
    }

    function stop() {
        $('#stop').prop('disabled', true);
        $('#start').prop('disabled', false);
        events.push({
            't': getSecElapsed(),
            'state': -1
        })
        clearInterval(loop);
        loop = undefined;
        locationid = $('#locationid').val() || 'data';
        saveJSON(`${locationid}.json`, JSON.stringify(events));
    }

    $('#locationid').on('input', function() {
        $('#start').prop('disabled', !Boolean($(this).val()));
    })
    $('#start').click(start);
    $('#stop').click(stop);
    $('#clicker').bind('mousedown touchstart', function() {
        events.push({
            't': getSecElapsed(),
            'state': 1
        })
        $('#clicker').addClass("active").html('Logging...');
    }).bind('mouseup touchend', function() {
        events.push({
            't': getSecElapsed(),
            'state': 0
        })
        $('#clicker').removeClass("active").empty();
    });
})