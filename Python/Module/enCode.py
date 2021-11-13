caesarChiper = {
	"ascii" : lambda message, shift:"".join([chr((ord(char) + shift - 32) % 96 + 32) for char in message]), 
	"ascii-all" : lambda message, shift:"".join([chr((ord(char) + shift) % 128) for char in message])
}