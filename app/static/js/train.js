document.addEventListener("DOMContentLoaded", async () => {
    const elem = document.getElementById('train-process');
    if (elem !== null) {
        let i = 0;
        const messages_str = document.getElementById('messages').innerText;
        const messages_arr = messages_str.split(',');
        for (const item of messages_arr) {
            await delay();
            elem.value = elem.value + item;
            if (i === messages_arr.length - 1) {
                await delay();
                document.querySelector('.use-button-block').style.display = 'block';
            }
            i++;
        }
    }
});

const delay = function() {
    return new Promise(resolve => setTimeout(resolve, 1000));
};