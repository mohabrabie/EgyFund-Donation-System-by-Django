let validateUrl = () => {
    const url = $("#facebook").val();
    var pattern = /^(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?$/;
    if( url && !pattern.test(url)) {
        alert("Incorrect Facebook URL");
    }
    return pattern.test(url);
}