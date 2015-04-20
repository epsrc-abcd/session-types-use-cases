package protocol;
class Protocol typestate ProtocolSession {
	private Alice a;
	private Bob b;

	Protocol() {
		a = new Alice();
		b = new Bob();
	}

	void AliceSaysHi() {
		a.sendStringToBob("Hi");
	}

	void BobReceivesGreet() {
		b.receiveStringFromAlice();
	}

	public static void main(String[] args) {
		Protocol p = new Protocol();
		p.AliceSaysHi();
		p.BobReceivesGreet();
	}
}
