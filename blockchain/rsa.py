from hashlib import sha256
x = 5
y = 1  # We don't know what y should be yet...

#while sha256(f'{x*y-(x-y*23*y*x)}'.encode()).hexdigest()[-3:] != "000":
while sha256(f'{x*y-(x-y*23*y*x)}'.encode()).hexdigest()[:5] != "00020":
    y += 1
print(f'The solution is y = {y}')
print(sha256(f'{x*y-(x-y*23*y*x)}'.encode()).hexdigest())
print(sha256(f'{x}{y}'.encode()).hexdigest())
print(sha256(f'{x*y-(x-y*23*y*x)}'.encode()).hexdigest()[:5])

