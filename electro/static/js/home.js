
function move(element)
{
    l=parseInt(window.getComputedStyle(element).left);
    t=parseInt(window.getComputedStyle(element).top);
    element.style.left=(l)+Math.random()*3+'px';
    element.style.top=(t+i*-10)+'px';
    element.style.animation = 'move '+time+'ms';
    element.style.left=(l)+'px';
    element.style.top=(t)+'px';
}


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
        
        time=call_to_brain(bottom_car,top_car)
        console.log("time computed",time);

        console.log()
        for (let i = 0; i < top_car; i++) {
            l=parseInt(window.getComputedStyle(top[i]).left);
            t=parseInt(window.getComputedStyle(top[i]).top);
            top[i].style.left=(l)//+Math.random()*10+'px';
            top[i].style.top=(t)//+i*-10)+'px';
            //console.log(top[i].style.top);
            top[i].style.animation = 'move '+time+'ms';
            //top[i].style.left=(l)+'px';
            //top[i].style.top=(t)+'px';
        }
        for (let i = 0; i < bottom_car; i++) {

            l=parseInt(window.getComputedStyle(bottom[i]).left);
            t=parseInt(window.getComputedStyle(bottom[i]).top);
            bottom[i].style.left=(l)//+Math.random()*10+'px';
            bottom[i].style.top=(t)//+i*10)+'px';
            bottom[i].style.animation = 'move '+time+'ms';
            //bottom[i].style.left=(l)+'px';
            //bottom[i].style.top=(t)+'px';
        }
        for (let i = 0; i < left_car; i++) {
            //l=parseInt(window.getComputedStyle(left[i]).left);
            //t=parseInt(window.getComputedStyle(left[i]).top);
            //left[i].style.left=(l)+i*10+'px';
            //left[i].style.top=(t)+Math.random()*3+'px';
            left[i].style.animation = null
            //left[i].style.left=l+'px';
            //left[i].style.top=t+'px';
        }
        for (let i = 0; i < right_car; i++) {

            //right[i].style.left=(parseInt(window.getComputedStyle(right[i]).left)+i*10)+'px';
            //right[i].style.top=(parseInt(window.getComputedStyle(right[i]).top)+Math.random()*3)+'px';
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

        time=time=call_to_brain(right_car,left_car);

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
            left[i].style.animation = 'move '+time+'ms'
        }
        for (let i = 0; i < right_car; i++) {
            right[i].style.animation = 'move '+time+'ms'
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


function call_to_brain(cars1,cars2)
{
    var time=0;
    var url='brain';
    var params = JSON.stringify({ cars1: 1, cars2:4});
    console.log(params);
    var xhr= new XMLHttpRequest();
    xhr.onreadystatechange=processRequest;
    function processRequest(e) {
        if(xhr.readyState==4 && xhr.status==200)
        {
            time=JSON.parse(xhr.responseText);
            console.log("time read : ",time['result']);
        }
        // body...
    }
    xhr.open('POST',url,false);//ATTENTION APPEL SYNCHRONE !!! NORMALEMENT IL FAUT GERER AVEC LES PROMESSSES
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("cars1="+cars1+"&cars2="+cars2);
    return time['result'];
}