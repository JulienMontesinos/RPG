def threaded_client(conn, player, players):
    conn.send(pickle.dumps(players))  # 初始发送所有玩家数据
    while True:
        try:
            # 接收来自客户端的数据
            data = pickle.loads(conn.recv(2048))
            players[player] = data  # 更新当前玩家的状态

            if not data:
                print("Disconnected")
                break
            else:
                # 准备要发送给客户端的所有玩家的数据
                reply = players

            # 发送所有玩家的数据
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()




currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # 启动新线程，传递玩家列表
    start_new_thread(threaded_client, (conn, currentPlayer, players))
    currentPlayer += 1
