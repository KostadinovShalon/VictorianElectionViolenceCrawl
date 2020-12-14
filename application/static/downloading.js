var isFinished = false

$(function (){
    statusPoll()
})

function statusPoll(){
    if(!isFinished){
        setTimeout(function() {
            $.ajax({
                url: "download/status",
                type: "GET",
                success: function (data) {
                    isFinished = data.finished
                    if (!isFinished) {
                        $('#search_text').text(data.search_text)
                        $('#start_date').text(data.start_date)
                        $('#end_date').text(data.end_date)
                        $('#downloaded_articles').text(data.downloaded_articles)
                        $('#total_articles').text(data.total_articles)
                    } else {
                        $('#downloaded_articles').text(data.downloaded_articles)
                        alert("Download finished")
                    }
                },
                error: function (data) {
                    isFinished = true
                    alert("Download error")
                },
                complete: statusPoll
            })
        }, 2000);
    }
}