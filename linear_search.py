# File: linear_search.py (Logika Algoritma)

# List global untuk menyimpan riwayat langkah
HISTORY = []

def linear_search(data_list, target):
    """
    Mengimplementasikan Linear Search dan mencatat setiap langkah di HISTORY.
    Mengembalikan index jika ditemukan, atau -1 jika tidak ditemukan.
    """
    global HISTORY
    HISTORY = []
    
    arr = data_list[:]
    n = len(arr)
    
    # Catat status awal
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'index': -1, # Index yang dicek
        'status': 'Mulai',
        'action': f'Memulai pencarian untuk nilai {target} secara sekuensial.'
    })

    for i in range(n):
        # Catat langkah pengecekan sebelum perbandingan
        HISTORY.append({
            'array': arr[:],
            'target': target,
            'index': i,
            'status': 'Mengecek',
            'action': f'Mengecek Indeks {i} (Nilai: {arr[i]})'
        })
        
        if arr[i] == target:
            # Catat langkah ditemukan
            HISTORY.append({
                'array': arr[:],
                'target': target,
                'index': i,
                'status': 'Ditemukan',
                'action': f'Nilai {target} DITEMUKAN pada Indeks {i}!'
            })
            return i, HISTORY
    
    # Catat langkah tidak ditemukan (HANYA setelah loop selesai sepenuhnya)
    HISTORY.append({
        'array': arr[:],
        'target': target,
        'index': -1,
        'status': 'Selesai',
        'action': f'Selesai. Nilai {target} tidak ditemukan dalam array setelah memeriksa {n} elemen.'
    })
    return -1, HISTORY
