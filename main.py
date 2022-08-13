import time
from transmission_rpc import Client

c = Client(host='localhost', port=9091, username='minigrim0', password='12345')

def remove_trackers():
    list_torrents = c.get_torrents()
    for torrent in list_torrents:
        if torrent.status == "downloading" and torrent.progress > 10.0:
            if torrent.trackers != []:
                c.change_torrent(torrent.id, trackerRemove=[tracker['id'] for tracker in torrent.trackers])


while True:
    time.sleep(60)  # Run every minute
    remove_trackers()

