import sqlite3
import os
import traceback

_db_path = os.path.normpath(os.path.join(os.getcwd(), "games.db"))

sqlite3.register_adapter(bool, int)
sqlite3.register_converter('BOOLEAN', lambda v: bool(int(v)))
sqlite3.register_converter('boolean', lambda v: bool(int(v)))

# I'm sure I'll never regret formatting the board like this.
_BOARD_START = "Br,Bn,Bb,Bq,Bk,Bb,Bn,Br,B,B,B,B,B,B,B,B,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,W,W,W,W,W,W,W,W,Wr,Wn,Wb,Wq,Wk,Wb,Wn,Wr"

def get_db_conn():
    if not os.path.exists(_db_path):
        return None, f"Database file does not exist: {_db_path}"
    
    conn = sqlite3.connect(_db_path)
    conn.row_factory = sqlite3.Row

    return conn, None

def create_game(inviter_name, inviter_id, invitee_name, invitee_id, inviter_wants_white=True):
    conn, _ = get_db_conn()

    # Check to make sure there aren't any current games with either of these users
    current_games = conn.execute("""
        SELECT *
        FROM Games
        WHERE player_1_user_id = ?
        OR player_1_user_id = ?
        OR player_2_user_id = ?
        OR player_2_user_id = ?;
    """, (inviter_id, invitee_id, inviter_id, invitee_id)).fetchall()

    if not current_games:
        # Create new game
        conn.execute("""
            INSERT INTO Games(player_1_name, player_1_user_id, player_2_name, player_2_user_id, white_user_id, current_turn_user_id, board)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (inviter_name, inviter_id, invitee_name, invitee_id, inviter_id if inviter_wants_white else invitee_id, inviter_id if inviter_wants_white else invitee_id, _BOARD_START))
        conn.commit()

        return True, ""
    else:
        return False, "One or both players are already in a game. Quit/forfeit that game via !quit/!forfeit before creating a new one."

def get_board(user_id):
    conn, _ = get_db_conn()

    return conn.execute("""
        SELECT board
        FROM Games
        WHERE player_1_user_id = ?
        OR player_2_user_id = ?
    """, (user_id, user_id)).fetchall()[0][0]
