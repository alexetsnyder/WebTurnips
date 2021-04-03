//Validate.js

class KeyValue
{
    constructor(keyValue) {
        const both = keyValue.split('=');
        this.key = both[0].trim();
        this.value = both[1].trim();
    }
}

class Cookies
{
    constructor() {
        self.cookies = {};
        if (document.cookie !== '')
        {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++)
            {
                let keyValue = new KeyValue(cookies[i].trim());
                self.cookies[keyValue.key] = keyValue.value;
            }
        }
    }

    get_cookie(name)
    {
        for (const key in self.cookies)
        {
            if (key === name)
            {
                return self.cookies[name];
            }
        }
        return null;
    }
}

// function CreateTippy(target, content)
// {
//     return tippy(target, {
//         theme: 'error',
//         arrow: true,
//         content: content,
//         delay: [0, 2000],
//         placement: 'bottom',
//         trigger: 'manual',
//     });
// }

function PostAjaxAsync(data, OnSuccess, OnError)
{
    const cookies = new Cookies();
    data['csrfmiddlewaretoken'] = cookies.get_cookie('csrftoken');
    const args = {
        type: 'POST',
        url: 'validate/',
        data: data,
        success: OnSuccess,
        error: OnError,
    };
    $.ajax(args);
}

function InjectErrorRows()
{
    $('tr').each(function () {
       let input_column_id = $(this).find('td > input')[0].id;
       let error_row_id = `${input_column_id}_ErrorRow`;
       $(this).append(`<td id=\"${error_row_id}\"></td>`);
    });
}

function GetFormData()
{
    let form_data = {}
    $('input').each(function () {
        const name = $(this).attr('name');
        if (name !== 'csrfmiddlewaretoken')
        {
            form_data[name] = $(this).val();
        }
    });
    return form_data;
}

function ShowErrors(errors)
{
    InjectErrorRows();
    for (let field in errors)
    {
        $(`#id_${field}_ErrorRow`).text(errors[field]);
    }
}

function AjaxSuccess(data) //, status, xhr)
{
    if (!$.isEmptyObject(data))
    {
        ShowErrors(data)
    }
    else
    {
        $('form').submit();
    }
}

function ValidateForm()
{
    const form_data = GetFormData();
    PostAjaxAsync(
        form_data,
        AjaxSuccess,
        function(xhr, status, data) {
            alert(`Ajax failed with status: ${status}`);
        },
    )
    return false;
}

function Init()
{
    $('#submit-button').click(ValidateForm);
}

$(function () {
    Init();
});