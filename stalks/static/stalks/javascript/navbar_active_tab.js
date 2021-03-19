function trim(string, trimChars)
{
    let fixedStr = string.replace(new RegExp('^' + trimChars + '+'), '');
    fixedStr = fixedStr.replace(new RegExp(trimChars + '+$'), '');
    return fixedStr;
}

//To do: Stalk week detail, add day price, add turnip stack, sell turnip stacks
$(function () {
    const path = trim(window.location.pathname, '/');
    console.log(path);
    const shldSlice = (new RegExp('.+/.+')).test(path);
    const file_name = trim(shldSlice ? path.slice(path.lastIndexOf('/')) : path, '/');
    $('.nav-link').each(function ()
    {
        $(this).removeClass("active");
    });
    console.log(file_name);
    switch (file_name)
    {
        case 'stalks':
            $('#navHomePageLink').addClass('active');
            break;
        case 'newweek':
            $('#navAddStalkWeekLink').addClass('active');
            break;
        default:
            $('#navHomePageLink').addClass('active');
    }
});