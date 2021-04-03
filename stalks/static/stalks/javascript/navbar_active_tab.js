function trim(string, trimChars)
{
    let fixedStr = string.replace(new RegExp('^' + trimChars + '+'), '');
    fixedStr = fixedStr.replace(new RegExp(trimChars + '+$'), '');
    return fixedStr;
}

function ChangeActiveNavbarLink()
{
    const path = trim(window.location.pathname, '/');
    const shldSlice = (new RegExp('.+/.+')).test(path);
    let file_name = trim(shldSlice ? path.slice(path.lastIndexOf('/')) : path, '/');
    //console.log(`Path: ${path} FileName: ${file_name}`);

    $('.nav-link').each(function ()
    {
        $(this).removeClass("active");
    });

    const detail_nbr = parseInt(file_name);
    if (!isNaN(detail_nbr))
    {
        $('#stalkItemDropdown').addClass('active');
    }
    else {
        switch (file_name) {
            case 'newweek':
                $('#navAddStalkWeekLink').addClass('active');
                break;
            case 'newprice':
                $('#navAddDayPrice').addClass('active');
                break;
            case 'newstacks':
                $('#navAddTurnipStacks').addClass('active');
                break;
            case 'sellstacks':
                $('#navSellTurnipStacks').addClass('active');
                break;
            default:
                $('#navHomePageLink').addClass('active');
        }
    }
}

$(function () {
    ChangeActiveNavbarLink();
});