package com.moosewarei.inc.medical.info.api;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.persistence.EntityManager;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.google.gson.Gson;
import com.maxud.listener.LocalEntityManagerFactory;

// A base class for all of the Medical information API classes.
public class MedicalInfoBase {
	protected Gson gson;
	protected EntityManager em;
	Logger logg = LoggerFactory.getLogger(this.getClass());
	
	public MedicalInfoBase() {
		gson = new Gson();
		em = LocalEntityManagerFactory.createEntityManager();
	}
	
	public void save(int keyField, Object o) throws Exception
	{
		em.getTransaction().begin();
		em.persist(o);
		em.getTransaction().commit();
		em.close();
	}

	public String readJson(InputStream incomingData) throws Exception{
		StringBuilder sb = new StringBuilder();
		BufferedReader in = new BufferedReader(new InputStreamReader(incomingData));
		String line = null;
		while ((line = in.readLine()) != null) {
			sb.append(line);
		}
		return sb.toString();
	}
	
}
