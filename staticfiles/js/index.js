window.addEventListener('scroll', function() {
    const containers = [
        document.getElementById('post'),
        document.getElementById('post2'),
        document.getElementById('news'),
        document.getElementById('footer')
    ];
    const windowHeight = window.innerHeight
    const scrollPosition = window.scrollY
    containers.forEach(container => {
        const divs = container.querySelectorAll('.item')
        divs.forEach(div => {
            const divTop = div.getBoundingClientRect().top + scrollPosition
            const divBottom = divTop + div.offsetHeight
            const start = scrollPosition
            const end = scrollPosition + windowHeight
            if (divBottom>start && divTop < end){
                div.classList.add('visible')
            } else {
                div.classList.remove('visible')
            }
        })
    })
})