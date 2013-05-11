import sys, platform

about = """
usage: {0} [file ...]

converts each file to an utf8 encoded file and suffixes its path with a ".utf8"
""".format(sys.argv[0]).strip()

codecs = """
euc_jp
euc_jis_2004
euc_jisx0213
""".split()
# from http://docs.python.org/3.3/library/codecs.html?highlight=codecs#standard-encodings

def main():
	if len(sys.argv) == 1:
		print(about)
		return

	for path in sys.argv[1:]:
		try:
			content = file_to_utf8(path)
			with open(path+".utf8", "w") as f:
				f.write(content)
		except MyError as e:
			print("can't convert {0}\n".format(path))
			print(e)

def file_to_utf8(path):
	with open(path, "rb") as f:
		t = f.read()
	decodings = []
	for codec in codecs:
		try:
			decodings.append((t.decode(codec), codec))
		except UnicodeDecodeError:
			pass
	if not decodings:
		raise MyError("no valid character set found")
	decoding = decodings[0][0]
	if not all(map(lambda d: decoding == d[0], decodings)):
		raise MyError("not all valid character sets result in the same unicode")
	return to_str(decoding)

def to_str(x):
	if platform.python_version_tuple()[0] == '2':
		return x.encode("utf8")
	else:
		return x

class MyError(Exception): pass

if __name__ == "__main__": main()
