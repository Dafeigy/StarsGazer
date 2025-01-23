function updateStatus(){
    document.getElementById("Sync").disabled = true
    console.log("Syncing Data Now...")
    $.ajax({
        url:"/updateStatus",
        type:"get",
        async: true,
        timeout: 10000,
        beforeSend:function(){
            $("#userinput").disabled = true
            document.getElementById("Sync").disabled = true
            $("#status").text(`Syncing now...`);
        },
        success:function (data) {
            document.getElementById("Sync").disabled = false
            $("#userinput").disabled= false
            $("#status").text(`Repo Nums: ${data.data}`);
            console.log(data)
        },
        error:function (data) {
            alert("Error getting starred repo information.")
            $('#userinput').disabled = false
            $("#status").text(`Error Fetching Data.`);
            document.getElementById("Sync").disabled = false
        },
    })
}

$("#Sync").click(function(){
    updateStatus()
})