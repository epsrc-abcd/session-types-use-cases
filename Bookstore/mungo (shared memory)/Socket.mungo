package demos.buyer_seller;

import java.util.LinkedList;

public class Socket {
	private LinkedList ep1_to_ep2 = new LinkedList();
	private LinkedList ep2_to_ep1 = new LinkedList();
	private Object endpoint1;
	private Object endpoint2;

	public void setEndpoints(Object endpoint1, Object endpoint2) {
		this.endpoint1 = endpoint1;
		this.endpoint2 = endpoint2;
	}

	public void send(Object from_endpoint, String message) {
		if (from_endpoint == endpoint1) {
			ep1_to_ep2.add(message);
		} else {
			ep2_to_ep1.add(message);
		}
	}

	public String receive(Object receiving_endpoint) {
    if (receiving_endpoint == endpoint1) {
        return (String)ep2_to_ep1.remove();
    } else {
        return (String)ep1_to_ep2.remove();
    }
 }

}