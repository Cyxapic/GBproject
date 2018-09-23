$(function(){
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    console.log(order_total_quantity, order_total_cost);

    for (let i=0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($(`input[name="orderitems-${i}-quantity"]`).val());
        _price = parseFloat($(`.orderitems-${i}-price`).text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }
    if (!order_total_quantity) {
        for (let i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }
    $('.order_form').on('click', 'input[type="number"]', function (event) {
        const target = event.target;
        orderitem_num = parseInt(target.name.split('-')[1]);
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }
    });
    $('.order_form').on('click', 'input[type="checkbox"]', function (event) {
        const target = event.target;
        orderitem_num = parseInt(target.name.split('-')[1]);
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });
    //**************************************************************************
    // add price product to order
    // НЕ ВЫШЕЛ КАМЕННЫЙ ЦВЕТОК
    $('.order_form').on('change', 'select', function (event) {
        const target = event.target;
        orderitem_num = parseInt(target.name.split('-')[1]);
        if (target.value) {
            $(`#id_orderitems-${orderitem_num}-quantity`).val(1);
            let priceTD = $(`#id_orderitems-${orderitem_num}-price`).closest('td');
            getPrice(target.value, priceTD, orderitem_num, );
        }
    });
    function getPrice(prodId, block, orderNum){
        const url = $('#url').attr('data-url');
        data = {
            csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
            prod_pk: prodId,
        }
        $.post(url, data).done(
            function (response) {
                let price = response.price;
                let tpl = `<span class="orderitems-${orderNum}-price">
                                ${price.replace('.', ',')}
                           </span> руб`;
                block.html(tpl);
                delta_quantity = 1;
                let total_forms = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
                $('input[name="orderitems-TOTAL_FORMS"]').val(total_forms + 1);
                TOTAL_FORMS = total_forms + 1;
                orderSummaryUpdate(price, delta_quantity);
                price_arr.push(price);
            }
        );
    }
    //**************************************************************************
    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;
        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }
    function deleteOrderItem(row) {
        var target_name= row[0].querySelector('input[type="number"]').name;
        orderitem_num = parseInt(target_name.split('-')[1]);
        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }
    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });
})