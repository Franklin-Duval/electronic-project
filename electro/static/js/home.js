
function lights(direction, top_car, bottom_car, left_car, right_car){
    
    //cars
    const top = document.getElementsByClassName('top-cars')[0].children;
    const bottom = document.getElementsByClassName('bottom-cars')[0].children;
    const left = document.getElementsByClassName('left-cars')[0].children;
    const right = document.getElementsByClassName('right-cars')[0].children;

    //lights
    const north_light = document.getElementsByClassName('north')[0].children;
    const south_light = document.getElementsByClassName('south')[0].children;
    const east_light = document.getElementsByClassName('east')[0].children;
    const west_light = document.getElementsByClassName('west')[0].children;

    let green_bright = 'rgb(0, 255, 0)'
    let orange_bright = 'rgb(255, 255, 0)'
    let red_bright = 'rgb(255, 0, 0)'

    let green_dark = 'rgb(77, 165, 77)'
    let orange_dark =  'rgb(151, 151, 54)'
    let red_dark = 'rgb(211, 87, 87)'

    if (direction === 'north'){
        let orange = 0
        north_light[0].style.backgroundColor = red_dark
        north_light[1].style.backgroundColor = orange_dark
        north_light[2].style.backgroundColor = green_bright

        south_light[0].style.backgroundColor = green_bright
        south_light[1].style.backgroundColor = orange_dark
        south_light[2].style.backgroundColor = red_dark

        west_light[0].style.backgroundColor = red_bright
        west_light[1].style.backgroundColor = orange_dark
        west_light[2].style.backgroundColor = green_dark

        east_light[0].style.backgroundColor = green_dark
        east_light[1].style.backgroundColor = orange_dark
        east_light[2].style.backgroundColor = red_bright

        for (let i = 0; i < top_car; i++) {
            top[i].style.animation = 'move 10000ms'
        }
        for (let i = 0; i < bottom_car; i++) {
            bottom[i].style.animation = 'move 10000ms'
        }
        for (let i = 0; i < left_car; i++) {
            left[i].style.animation = null
        }
        for (let i = 0; i < right_car; i++) {
            right[i].style.animation = null
        }
        setInterval(() => {
            orange = orange + 1
            if (orange === 7){
                north_light[1].style.backgroundColor = orange_bright
                north_light[2].style.backgroundColor = green_dark

                south_light[0].style.backgroundColor = green_dark
                south_light[1].style.backgroundColor = orange_bright
                clearInterval()
            }
        }, 1000)
    }
    else{
        let orange = 0
        north_light[0].style.backgroundColor = red_bright
        north_light[1].style.backgroundColor = orange_dark
        north_light[2].style.backgroundColor = green_dark

        south_light[0].style.backgroundColor = green_dark
        south_light[1].style.backgroundColor = orange_dark
        south_light[2].style.backgroundColor = red_bright

        west_light[0].style.backgroundColor = red_dark
        west_light[1].style.backgroundColor = orange_dark
        west_light[2].style.backgroundColor = green_bright

        east_light[0].style.backgroundColor = green_bright
        east_light[1].style.backgroundColor = orange_dark
        east_light[2].style.backgroundColor = red_dark

        for (let i = 0; i < top_car; i++) {
            top[i].style.animation = null
        }
        for (let i = 0; i < bottom_car; i++) {
            bottom[i].style.animation = null
        }
        for (let i = 0; i < left_car; i++) {
            left[i].style.animation = 'move 10000ms'
        }
        for (let i = 0; i < right_car; i++) {
            right[i].style.animation = 'move 10000ms'
        }

        setInterval(() => {
            orange = orange + 1
            if (orange === 7){
                east_light[1].style.backgroundColor = orange_bright
                east_light[0].style.backgroundColor = green_dark

                west_light[2].style.backgroundColor = green_dark
                west_light[1].style.backgroundColor = orange_bright
                clearInterval()
            }
        }, 1000)
    }

}

function lighting(top, bottom, left, right){
    let second = 1
    let minute = 0

    setInterval(() => {
        timer(minute, second)
        second = second + 1
        if (second === 60){
            second = 0
            minute = minute + 1
        }
    }, 1000)
    
    i = 1
    lights('north', top, bottom, left, right)
    setInterval(() => {
        lights(i%2==0 ? 'north' : 'east', top, bottom, left, right)
        i=i+1
    }, 10000)
}

function timer(m, s){
    const sec = document.getElementById('sec')
    const min = document.getElementById('min')

    min.textContent = m
    sec.textContent = s
}