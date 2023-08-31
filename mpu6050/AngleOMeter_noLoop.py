#Connections
#MPU6050 - Raspberry pi
#VCC - 5V  (2 or 4 Board)
#GND - GND (6 - Board)
#SCL - SCL (5 - Board)
#SDA - SDA (3 - Board)

from .Kalman import KalmanAngle
import smbus                    #import SMBus module of I2C
import time
import math

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

kalmanZ = KalmanAngle()
kalmanY = KalmanAngle()

RestrictPitch = True    #Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
radToDeg = 57.2957786
kalAngleZ = 0
kalAngleY = 0

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


#Read the gyro and acceleromater values from MPU6050
def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(DeviceAddress, SMPLRT_DIV, 7)

    #Write to power management register
    bus.write_byte_data(DeviceAddress, PWR_MGMT_1, 1)

    #Write to Configuration register
    #Setting DLPF (last three bit of 0X1A to 6 i.e '110' It removes the noise due to vibration.) https://ulrichbuschbaum.wordpress.com/2015/01/18/using-the>    bus.write_byte_data(DeviceAddress, CONFIG, int('0000110',2))

    #Write to Gyro configuration register
    bus.write_byte_data(DeviceAddress, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(DeviceAddress, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(DeviceAddress, addr)
        low = bus.read_byte_data(DeviceAddress, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

bus = smbus.SMBus(11)   # or bus = smbus.SMBus(0) for older version boards
DeviceAddress = 0x68   # MPU6050 device address

MPU_Init()

time.sleep(1)
#Read Accelerometer raw value
accX = read_raw_data(ACCEL_XOUT_H)
accY = read_raw_data(ACCEL_YOUT_H)
accZ = read_raw_data(ACCEL_ZOUT_H)

#print(accX,accY,accZ)
#print(math.sqrt((accY**2)+(accZ**2)))
if (RestrictPitch):
    roll = math.atan2(accY,accX) * radToDeg
    pitch = math.atan(-accZ/math.sqrt((accY**2)+(accX**2))) * radToDeg
else:
    roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
    pitch = math.atan2(-accX,accZ) * radToDeg
# print(roll)

kalmanZ.setAngle(roll)
kalmanY.setAngle(pitch)
gyroZAngle = roll;
gyroYAngle = pitch;
compAngleZ = roll;
compAngleY = pitch;

timer = time.time()
flag = 0

#Read Angle function
def angle_read():
    global kalAngleZ, kalAngleY, RestrictPitch, radToDeg
    global bus, DeviceAddress

    global gyroZAngle, gyroYAngle, compAngleZ, compAngleY, timer, flag
    if(flag >100): #Problem with the connection
        print("There is a problem with the connection")
        flag=0
        # continue
    try:
        #Read Accelerometer raw value
        accX = read_raw_data(ACCEL_XOUT_H)
        accY = read_raw_data(ACCEL_YOUT_H)
        accZ = read_raw_data(ACCEL_ZOUT_H)

        #Read Gyroscope raw value
        gyroX = read_raw_data(GYRO_XOUT_H)
        gyroY = read_raw_data(GYRO_YOUT_H)
        gyroZ = read_raw_data(GYRO_ZOUT_H)

        dt = time.time() - timer
        timer = time.time()

        if (RestrictPitch):
            roll = math.atan2(accY,accX) * radToDeg
            pitch = math.atan(-accZ/math.sqrt((accY**2)+(accX**2))) * radToDeg
        else:
            roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
            pitch = math.atan2(-accX,accZ) * radToDeg

        gyroZRate = gyroZ/131
        gyroYRate = gyroY/131
      
        if (RestrictPitch):

            if((roll < -90 and kalAngleZ >90) or (roll > 90 and kalAngleZ < -90)):
                kalmanZ.setAngle(roll)
                complAngleZ = roll
                kalAngleZ   = roll
                gyroZAngle  = roll
            else:
                kalAngleZ = kalmanZ.getAngle(roll,gyroZRate,dt)

            if(abs(kalAngleZ)>90):
                gyroYRate  = -gyroYRate
                kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
        else:
            if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
                kalmanY.setAngle(pitch)
                complAngleY = pitch
                kalAngleY   = pitch
                gyroYAngle  = pitch
            else:
                kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)

            if(abs(kalAngleY)>90):
                gyroZRate  = -gyroZRate
                kalAngleZ = kalmanZ.getAngle(roll,gyroZRate,dt)

        #angle = (rate of change of angle) * change in time
        gyroZAngle = gyroZRate * dt
        gyroYAngle = gyroYAngle * dt

        #compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
        compAngleZ = 0.93 * (compAngleZ + gyroZRate * dt) + 0.07 * roll
        compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch

        if ((gyroZAngle < -180) or (gyroZAngle > 180)):
            gyroZAngle = kalAngleZ

        if ((gyroYAngle < -180) or (gyroYAngle > 180)):
            gyroYAngle = kalAngleY
        # print("Angle Z: " + str(kalAngleZ) + "   " + "Angle Y: " + str(kalAngleY))

        # print("Angle Z: {:.2f}   Angle Y: {:.2f}".format(kalAngleZ, compAngleY))



        #print(str(roll)+"  "+str(gyroXAngle)+"  "+str(compAngleX)+"  "+str(kalAngleX)+"  "+str(pitch)+"  "+str(gyroYAngle)+"  "+str(compAngleY)+"  "+str(k>

        return kalAngleZ

    except Exception as exc:
        flag += 1



print(angle_read())


