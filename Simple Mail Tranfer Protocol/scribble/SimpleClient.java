package demo.smtp;

import static demo.smtp.Smtp.Smtp.Smtp.C;
import static demo.smtp.Smtp.Smtp.Smtp.S;
import static demo.smtp.Smtp.Smtp.Smtp._220;
import static demo.smtp.Smtp.Smtp.Smtp._235;
import static demo.smtp.Smtp.Smtp.Smtp._250;
import static demo.smtp.Smtp.Smtp.Smtp._250d;
import static demo.smtp.Smtp.Smtp.Smtp._354;
import static demo.smtp.Smtp.Smtp.Smtp._501;
import static demo.smtp.Smtp.Smtp.Smtp._535;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Base64;

import org.scribble.net.Buf;
import org.scribble.net.scribsock.LinearSocket;
import org.scribble.net.session.SSLSocketChannelWrapper;
import org.scribble.net.session.SessionEndpoint;
import org.scribble.net.session.SocketChannelEndpoint;

import demo.smtp.Smtp.Smtp.Smtp;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_1;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_10;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_11_Cases;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_4;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_6;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_8;
import demo.smtp.Smtp.Smtp.channels.C.Smtp_C_9_Cases;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Branch_C_S_250__S_250d;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Case_C_S_250__S_250d;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Select_C_S_Auth__S_Quit;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Select_C_S_Ehlo__S_Quit;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Select_C_S_Quit__S_StartTls;
import demo.smtp.Smtp.Smtp.channels.C.ioifaces.Succ_In_S_250;
import demo.smtp.Smtp.Smtp.roles.C;
import demo.smtp.message.SmtpMessageFormatter;
import demo.smtp.message.client.Auth;
import demo.smtp.message.client.Data;
import demo.smtp.message.client.DataLine;
import demo.smtp.message.client.Ehlo;
import demo.smtp.message.client.EndOfData;
import demo.smtp.message.client.Mail;
import demo.smtp.message.client.Quit;
import demo.smtp.message.client.Rcpt;
import demo.smtp.message.client.StartTls;
import demo.smtp.message.client.Subject;

public class SimpleClient
{
	public SimpleClient() throws Exception
	{
		run();
	}

	public void run() throws Exception
	{
		String host = "...";
		int port = 25;

		String ehlo = "...";
		String mail = "...";  // Sender
		String rcpt = "...";
		String subj = "...";
		String body = "...";

		Smtp smtp = new Smtp();
		try (SessionEndpoint<Smtp, C> se = new SessionEndpoint<>(smtp, C, new SmtpMessageFormatter()))
		{
			se.connect(S, SocketChannelEndpoint::new, host, port);

			Smtp_C_11_Cases cases =
					doAuth(
						doEhlo(
							doStartTls(
								doEhlo(new Smtp_C_1(se).async(S, _220), ehlo)
							)
						, ehlo))
					.send(S, new Mail(mail))
					.branch(S);
			switch (cases.getOp())
			{
				case _250:
				{
					cases.receive(_250)
						.send(S, new Rcpt(rcpt))
						.async(S, _250)
						.send(S, new Data())
						.async(S, _354)
						.send(S, new Subject(subj))
						.send(S, new DataLine(body))
						.send(S, new EndOfData())
						.receive(S, _250, new Buf<>())
						//.async(S, _250)
						.send(S, new Quit());
					break;
				}
				case _501:
				{
					cases.receive(_501).send(S, new Quit());
				}
			}
		}
	}

	private <S1 extends Succ_In_S_250, S2 extends Branch_C_S_250__S_250d<S1, S2>>
			//S1 doEhlo(Select_C_S_Ehlo__S_Quit<S2, ?> s, String ehlo) throws Exception
			S1 doEhlo(Select_C_S_Ehlo<S2> s, String ehlo) throws Exception
	{
		Branch_C_S_250__S_250d<S1, S2> bra = s.send(S, new Ehlo(ehlo));
		while (true)
		{
			Case_C_S_250__S_250d<S1, S2> cases = bra.branch(S);
			switch (cases.getOp())
			{
				case _250:
				{
					return cases.receive(_250);
				}
				case _250d:
				{
					bra = cases.receive(_250d);
					break;
				}
			}
		}
	}

	private Smtp_C_6 doStartTls(Smtp_C_4 s4) throws Exception
	{
		return
				LinearSocket.wrapClient(
						s4.send(S, new StartTls())
							.async(S, _220)
				, S, SSLSocketChannelWrapper::new);
	}

	private Smtp_C_10 doAuth(Smtp_C_8 s8) throws Exception
	{
		Smtp_C_9_Cases s9cases = s8.send(S, new Auth(getAuthPlain())).branch(S);
		switch (s9cases.op)
		{
			case _235:
			{
				return s9cases.receive(_235);
			}
			case _535:
			{
				s9cases.receive(_535).send(S, new Quit());
				System.exit(0);
			}
			default:  // To satisfy Java typing for return
			{
				throw new RuntimeException("Won't get in here: " + s9cases.op);
			}
		}
	}

	private String getAuthPlain() throws IOException
	{
		return ...;
	}

	public static void main(String[] args) throws Exception
	{
		new SimpleClient();
	}
}

