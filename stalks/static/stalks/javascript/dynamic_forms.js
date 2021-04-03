//dynamic_forms.js

class Pair
{
    constructor(first, second) {
        this.first = first;
        this.second = second;
    }
}

function get_pair(string, splitChar=' ')
{
    let pairList = string.split(splitChar);
    return new Pair(pairList[0], pairList[1]);
}

function AddTableRow(tableId) {
    let tableSelector = $(tableId);
    let tableRowsSelector = tableSelector.find('tr');
    let rowCount = tableRowsSelector.length - 1;
    let lastRowSelector = tableRowsSelector.last();

    console.log(`Rows: ${rowCount}`);

    let lastRowClone = lastRowSelector.clone();
    let tdsInRowCloneSelector = lastRowClone.find('td');

    tdsInRowCloneSelector.each(function() {
        let inputSelector = $(this).find('input').last();
        if (inputSelector.exists())
        {
            let inputName = inputSelector.attr('name');
            let inputNamePair = get_pair(inputName, `${rowCount - 1}`);
            let newName = `${inputNamePair.first}${rowCount}${inputNamePair.second}`
            let newId = `id_${inputNamePair.first}${rowCount}${inputNamePair.second}`
            console.log(newName);

            inputSelector.attr('name', newName);
            inputSelector.attr('id', newId);
        }
        else
        {
            let btnSelector = $(this).find('button').last();
            if (btnSelector.exists())
            {
                let delBtn = btnSelector.clone();
                btnSelector.remove();
                $(delBtn).removeClass('btn-success')
                         .addClass('btn-danger')
                         .find('i').last()
                         .removeClass('fa-plus')
                         .addClass('fa-times');
                $(delBtn).click(function () {
                    $(tableId).find('tr').last().remove();
                });
                $(this).append(delBtn);
            }
        }
    });
    lastRowSelector.after(lastRowClone);
    tableSelector.find('tr')
                 .last()
                 .find('.datepicker')
                 .removeClass('hasDatepicker')
                 .datepicker({dateFormat: 'MM dd yy'});
    return false;
}

function AddTurnipStacksRow()
{
    return AddTableRow('#turnip-stacks-forms');
}

function AddDayPriceRow()
{
    return AddTableRow('#day-price-forms');
}


$(function () {
    $.fn.exists = function () {
        return this.length !== 0;
    }
    $('#add-turnip-row').click(AddTurnipStacksRow);
    $('#add-day-price-row').click(AddDayPriceRow);
});