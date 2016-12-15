extern crate testpi;
use testpi::pigpio;

fn main() {
    let pi = pigpio::Pi::new();
    pi.set_mode(32, pigpio::OUTPUT);
    let on_time = 40;
    let time_period = 80;
    println!("Frequency: {}", 1000/time_period);
    let mut total_flashes = 60;
    while total_flashes > 0 {
        total_flashes -= 1;
        pi.write(32, 1);
        pigpio::sleep_ms(on_time);
        pi.write(32, 0);
        pigpio::sleep_ms(time_period-on_time);
    }
}

/*fn main() {
    let pi = pigpio::Pi::new();
    pi.set_mode(25, pigpio::OUTPUT);
    pi.set_mode(18, pigpio::INPUT);
    pi.set_pull_up_down(18, pigpio::PUD_DOWN);
    let mut blips: i64 = 0;
    let mut blip_ready = true;
    pi.write(25, 1);
    loop {
        /* println!("Currently {}", match pi.read(18) {
                                    1 => "light",
                                    0 => "dark",
                                    _ => "error",
                                 });
        */
        if pi.read(18) == 1 {
            if blip_ready {
                blips += 1;
                blip_ready = false;
                // if blips % 10 == 0 {
                println!("Blip {}", blips);
                // }
            }
        } else {
            blip_ready = true;
        }
        pigpio::sleep_ms(1);
    }
}
*/
