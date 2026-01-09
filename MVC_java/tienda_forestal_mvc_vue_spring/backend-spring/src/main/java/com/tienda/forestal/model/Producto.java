package com.tienda.forestal.model;

import jakarta.persistence.*;

@Entity
@Table(name = "productos")
public class Producto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String nombre;
    private String tipo;
    private String marca;
    private String descripcion;
    private Double precio;
    private int stock;
    private String imagen;

    // Getters y setters
}

