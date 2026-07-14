$(document).ready(function () {
    $('#submit-btn').on('click', function () {
        let sepal_length = $('#sepal_length').val();
        let sepal_width = $('#sepal_width').val();
        let petal_length = $('#petal_length').val();
        let petal_width = $('#petal_width').val();

        // 유효성 검사
        if (sepal_length == '' || sepal_width == '' || petal_length == '' || petal_width == '') {
            alert('모든 필드를 입력해주세요.');
            return;
        }

        var request_data = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }

        $.ajax({
            url: '/api/ai/iris',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(request_data),
            success: function (response) {
                if (!response.success) {
                    alert(response.message || '예측에 실패했습니다.');
                    return;
                }

                console.log(response);

                var species = response.class_name;
                var confidence = response.confidence_score;

                $('#result-species').text(species);
                $('#result-confidence').text(confidence.toFixed(1) + '%');
                $('#result-message').text(response.message);
                $('#confidence-fill').css('width', confidence + '%');

                $('.tag').removeClass('active');
                $('.tag[data-species="' + species + '"]').addClass('active');

                $('#iris-result')
                    .removeClass('is-setosa is-versicolor is-virginica')
                    .addClass('is-' + species)
                    .prop('hidden', false);
            },
            error: function () {
                alert('서버 요청 중 오류가 발생했습니다.');
            },
        });
    });
});
