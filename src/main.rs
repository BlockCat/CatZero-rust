extern crate cpython;
extern crate hashbrown;

mod pyenv;
mod model;
mod mcts;
mod game;

use pyenv::PyEnv;
use game::tictactoe::{TicTacToe, AlphaAgent, PlayerAgent, TicTacToeState, TicTacToeAction};
use game::Game;
use mcts::MCTS;

fn main() {
    let mut env = PyEnv::new();
    let python = env.python();
    let sys = python.import("sys").unwrap();
    let version: String = sys.get(python, "version").unwrap().extract(python).unwrap();
    
    println!("Version: {}", version);

    let nn = match model::CatZeroModel::new(&python, (5, 3, 3), (1, 3, 3), 0.1, 2) {
        Ok(e) => e,
        Err(e) => {
            e.print(python);
            return;
        }
    };
    //nn.save("saved_model.h5").unwrap();

    // let agent1 = PlayerAgent;
    // let agent2 = PlayerAgent;
    // let ttt = TicTacToe::new(agent1, agent2);
    // ttt.start();

    let def = TicTacToeState::default();
    let mcts: MCTS<TicTacToeState, TicTacToeAction> = mcts::MCTS::new(&nn).time_limit(Some(1000));

    let action = mcts.search(def);

    println!("Best action: {:?}", action);

    //let result: String = nn.call(python, "create_model", cpython::NoArgs, None).unwrap().extract(python).unwrap();

    //println!("Result: {}", result);    
}