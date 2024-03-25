import { useState } from "react";

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}
export default function Game() {
  const [history, setHistory] = useState([Array(9).fill(null)]);
  //creates an array, where the first element is an array of nil
  const [currentMove, setCurrentMove] = useState(0);
  const currentSquares = history[currentMove];
  const xIsNext = currentMove % 2 === 0;

  function handlePlay(nextSquares) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares];
    setHistory(nextHistory);
    setCurrentMove(nextHistory.length - 1);  
  }


  function jumpTo(nextMove) {
    setCurrentMove(nextMove);
  }
  const moves = history.map((squares, move) => {
    let description;
    if (move > 0) {
      description = "Go to move #" + move;
    } else {
      description = "Go to game start";
    }

    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    );
  });
  if(moves){};

  return (
    <div className="game">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} currentMove={currentMove} />
      </div>
      {/* <div>
        <ol> {moves} </ol>
      </div> */}
    </div>
  );
}

function Board({ xIsNext, squares, onPlay, currentMove }) {
  const [selectMode, setSelectMode] = useState(true);
  const [selectPiece, setSelectPiece] = useState(0);

  function handleClick(i) {
    console.log(i);

    //State 0 - THERE IS A WINNER, GAME IS OVER 
    if (calculateWinner(squares)) {return;}
    const nextSquares = squares.slice();

    //STATE 1 - FIRST 3 MOVES, PLACING
    if(currentMove < 6){
      if(squares[i]) {
        return; //First three turns – ONLY PLACING DOWN
      }

      if (xIsNext) {
        nextSquares[i] = "X";
      } else {
        nextSquares[i] = "O";
      }
      onPlay(nextSquares);
    } 
    //STATE 2 - EVERY OTHER MOVE
    else {
      //STATE 2.1 - SELECTING a piece to move
      if(selectMode){
        if((((squares[i] === "X") && (xIsNext))) || ((squares[i] === 'O') && (!xIsNext))) {
          setSelectPiece(i);
          setSelectMode(false); //Now it's time to move that piece baby
        } else {
          //selected the wrong piece, get outta here
          return;
        }
      }

      //STATE 2.2 - MOVING that piece
      else {
        setSelectMode(true);

        //Requested square is already occupied
        if(squares[i]){return;}

        //Check the requested spot is available
        if(isValid(selectPiece, i)){
          
          //Check if center piece is occupied by your piece
          if((((squares[4] === "X") && (xIsNext))) || ((squares[4] === 'O') && (!xIsNext))){

            console.log("MUST MOVE")
            //Check if the position would win
            let tempSquares = nextSquares;
            if (xIsNext) {
              tempSquares[i] = "X";
            } else {
              tempSquares[i] = "O";
            }
            // console.log("Select piece: ", selectPiece);
            // console.log("Select piece === 4: ", selectPiece === 4);
            // console.log("calculate winner: ", calculateWinner(tempSquares));
            // console.log("Required piece: ", i);

            if(selectPiece === 4 || calculateWinner(tempSquares) != null) {
              // console.log("TURE??")
              if (xIsNext) {
                nextSquares[i] = "X";
              } else {
                nextSquares[i] = "O";
              }
              nextSquares[selectPiece] = null;
            } else {
              console.log("Center piece is occupied. Must win or vacate center");
              return;
            }
          } else {
            //If you don't have a piece in the center, you can do whateva
            if (xIsNext) {
              nextSquares[i] = "X";
            } else {
              nextSquares[i] = "O";
            }
            nextSquares[selectPiece] = null;
          }
          
        } else {
          return;
        }
       
        onPlay(nextSquares);
      }
    }



  }

  //Check if someone has won
  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = "Winner: " + winner;
  } else {
    status = "Next player: " + (xIsNext ? "X" : "O");
  }
  
  
  //Return the board
  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}



function isValid(currPos, r) {
  let validPos = false;
  //r is short for requestedPosition
  //there could be some logic here but i'm just brute forcing it, there are only 9 spots
  switch (currPos){
    case 0:
      validPos = (r === 1 || r === 3 || r === 4);
      break;
    case 1:
      validPos = (r === 0 || r === 2 || r === 3 || r === 4 || r === 5);
      break;
    case 2:
      validPos = (r === 1 || r === 4 || r === 5);
      break;
    case 3:
      validPos = (r === 0 || r === 1 || r === 4 || r === 6 || r === 7);
      break;
    case 4:
      validPos = true;
      break;
    case 5:
      validPos = (r === 1 || r === 2 || r === 4 || r === 7 || r === 8);
      break;
    case 6:
      validPos = (r === 3 || r === 4 || r === 7);
      break;
    case 7:
      validPos = (r === 3 || r === 5 || r === 4 || r === 6 || r === 8);
      break;
    case 8:
      validPos = (r === 7 || r === 4 || r === 5);
      break;
    default:
      validPos = false;
  }
  return validPos;
}


//Keep this function
function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
